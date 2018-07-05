from constants import Constants


class ConstraintManager(object):

    def __init__(self, monitored_area):
        self.monitored_area = monitored_area

    @staticmethod
    def c3_neighbors_sync(vi, vj):
        diff = abs(vi - vj)
        if 0 < diff <= Constants.T_SYNCHRO:
            return 1
        return 0

    def get_cost_of_private_constraints_for_value(self, value):
        return self.c1_no_devices(value) \
               + self.c2_device_status(value) \
               + self.c4_last_intervention(value) \
               + self.c5_nothing_to_report(value)

    def get_cost_of_private_constraints_for_zone(self, value):

        cost = 0

        for room in self.monitored_area.monitored_area_list:

            cm = ConstraintManager(room)

            if room.is_in_critical_state():
                return 0 if value == 0 else Constants.INFINITY

            cost += cm.c4_last_intervention(value)
            cost += cm.c2_device_status(value)

        return cost if cost < Constants.INFINITY else Constants.INFINITY

    def c1_no_devices(self, vi):
        if self.monitored_area.has_no_devices() and vi < Constants.INFINITY:
            print("no devices")
            return Constants.INFINITY
        return 0

    def c2_device_status(self, vi):

        if self.monitored_area.is_in_critical_state():
            if vi > 0:
                print("critic state")
                return Constants.INFINITY
        else:
            min_end_of_prog = self.monitored_area.get_min_end_of_prog()
            if min_end_of_prog <= Constants.URGT_TIME and vi > min_end_of_prog:
                return 1

        return 0

    def c4_last_intervention(self, vi):
        if self.monitored_area.is_tau_too_high() and vi > Constants.URGT_TIME:
            print("tau too high")
            return Constants.INFINITY
        return 0

    def c5_nothing_to_report(self, vi):

        if not self.monitored_area.is_in_critical_state() \
                and self.monitored_area.get_min_end_of_prog() > Constants.URGT_TIME \
                and self.monitored_area.tau < Constants.THREE_HOURS \
                and vi < Constants.INFINITY:
            return 1

        return 0
