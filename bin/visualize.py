import datetime

class Visualization:
    COLOR_EMPTY = 'D8D8D8'
    COLOR_NORMAL = 'b3ffb3'
    COLOR_OVERLAP = 'ff9999'
    # COLOR_MINIMAL = 'BEBEBE'

    def __init__(self, slots, frequencies, nds, parents, omega):
        self.nr_slots = slots
        self.nr_frequencies = frequencies
        self.nodes = nds
        self.parents = parents
        self.reliability = {}
        self.omega = omega
        self.parents[0] = 'NA'
        self.reliability[0] = 'NA'
        # self.minimal_slots = minimal_slots
        self.nodes_sigma = {}
        self.nodes_beta = {}
        self.nodes_arr = {}
        self.nodes_delta = {}
        self.schedule = {}
        self.arr_root_list = []
        self.x_list = []
        self.sl = None # total amount of slots
        self.available_slots = None # number of available slots
        self.obj_val = None

        for slot in range(slots):
            for frequency in range(frequencies):
                self.schedule[slot, frequency] = []

    def add_sigma(self, t, f, n, s):
        for _t in range(t, t + s):
            self.schedule[_t, f].append((t, f, n, s))

        if n not in self.nodes_sigma:
            self.nodes_sigma[n] = []
        self.nodes_sigma[n].append((t, f, n, s))

    def add_beta(self, r, m, n):
        if n not in self.nodes_beta:
            self.nodes_beta[n] = []
        self.nodes_beta[n].append((r, m, n))

    def add_reliability(self, n, reliability):
        if n in self.reliability:
            assert False # should only be one reliability
        self.reliability[n] = reliability

    def add_arr(self, n, solution):
        if n not in self.nodes_arr:
            self.nodes_arr[n] = []
        self.nodes_arr[n].append((solution))

    def add_delta(self, n, solution):
        if n not in self.nodes_delta:
            self.nodes_delta[n] = []
        self.nodes_delta[n].append((solution))

    def add_obj_val(self, obj_val):
        self.obj_val = obj_val

    def add_arr_root_list(self, lst):
        self.arr_root_list = lst

    def add_x_list(self, lst):
        self.x_list = lst

    def add_total_slots(self, sl):
        self.sl = sl

    def add_available_slots(self, sl):
        self.available_slots = sl

    def visualize(self, suffix):
        output = '<html><head><title>ADAPTSCH ILP solution</title></head><body style="font-family:arial;">'

        ### show schedule
        output += '<h1>ILP output at: %s</h1>' % str(datetime.datetime.now())
        output += '<h1>Schedule</h1><table border="0" cellpadding="5" style="font-size:11px;">'
        output += '<tr><th width="100" height="25" bgcolor="#F0F0F0">/</th>'
        for slot in range(self.nr_slots):
            color = 'F0F0F0'
            # if slot in self.minimal_slots:
            #     color = self.COLOR_MINIMAL
            output += '<th width="100" height="25" bgcolor="#%s">%s</th>' % (color, slot)
        output += '</tr>'
        for frequency in range(self.nr_frequencies):
            output += '<tr><th width="100" height="25" bgcolor="#F0F0F0">%s</th>' % (frequency)
            for slot in range(self.nr_slots):
                data = ''
                for (t, f, n, s) in self.schedule[slot, frequency]:
                    data += '&sigma;(n: %s, t: %s, f: %s, s: %s)</br>' % (n, t, f, s)
                color = self.COLOR_EMPTY
                if len(self.schedule[slot, frequency]) > 1:
                    color = self.COLOR_OVERLAP
                elif len(self.schedule[slot, frequency]) == 1:
                    color = self.COLOR_NORMAL
                output += '<td width="100" height="25" bgcolor="#%s"><center>%s</center></td>' % (color, data)
            output += '</tr>'
        output += '</table></font>'

        ### show node

        output += '<h1>Decision variables</h1><table border="0" cellpadding="5" style="font-size:11px;">'
        output += '<tr><th width="100" height="25" bgcolor="#F0F0F0">Node</th><th width="100" height="25" bgcolor="#F0F0F0">Parent</th><th width="100" height="25" bgcolor="#F0F0F0">Reliability</th><th width="100" height="25" bgcolor="#F0F0F0">&beta;(r,m,n)</th><th width="100" height="25" bgcolor="#F0F0F0">&sigma;(t,f,n,s)</th><th width="100" height="25" bgcolor="#F0F0F0">&delta;(n)</th><th width="100" height="25" bgcolor="#F0F0F0">arr(n)</th></tr>'
        for n in self.nodes:
            output += '<tr>'
            output += '<td width="100" height="25" bgcolor="#F0F0F0"><center>%s</center></td>' % (n)
            output += '<td width="100" height="25" bgcolor="#F0F0F0"><center>%s</center></td>' % (self.parents[n])
            output += '<td width="100" height="25" bgcolor="#F0F0F0"><center>%s</center></td>' % (self.reliability[n])
            tmp_nodes_beta = '/'
            if n in self.nodes_beta:
                tmp_nodes_beta = ''
                for s in self.nodes_beta[n]:
                    tmp_nodes_beta += '%s</br>' % (str(s))
            output += '<td width="125" height="25" bgcolor="#F0F0F0"><center>%s</center></td>' % (tmp_nodes_beta)
            tmp_nodes_sigma = '/'
            if n in self.nodes_sigma:
                tmp_nodes_sigma = ''
                for s in self.nodes_sigma[n]:
                    tmp_nodes_sigma += '%s</br>' % (str(s))
            output += '<td width="100" height="25" bgcolor="#F0F0F0"><center>%s</center></td>' % (tmp_nodes_sigma)
            tmp_nodes_delta = '/'
            if n in self.nodes_delta:
                tmp_nodes_delta = ''
                for s in self.nodes_delta[n]:
                    tmp_nodes_delta += '%s</br>' % (str(s))
            output += '<td width="100" height="25" bgcolor="#F0F0F0"><center>%s</center></td>' % (tmp_nodes_delta)
            tmp_nodes_arr = '/'
            if n in self.nodes_arr:
                tmp_nodes_arr = self.nodes_arr[n]
            output += '<td width="100" height="25" bgcolor="#F0F0F0"><center>%s</center></td>' % (tmp_nodes_arr)
            output += '</tr>'
        output += '</table></font>'

        output += '<h1>Objective function (omega = %.1f)</h1>' % self.omega

        total_arr = 0.0
        for (c, arr_child) in self.arr_root_list:
            total_arr += arr_child

        total_x = 0.0
        for (c, x_child) in self.x_list:
            total_x += x_child

        output += '<h3><sup>sum(Arr)</sup>&frasl;<sub>sum(x_n)</sub> = <sup>%.4f</sup>&frasl;<sub>%.4f</sub> = %.4f</h3>' % (total_arr, total_x, (total_arr / float(total_x)))

        output += '<h3><sup>RadioTime</sup> &frasl; <sub>|T| * SLOT_LENGTH * |N_0|</sub> = <sup>%.4f</sup> &frasl; <sub>%.4f</sub> = %.4f</h3>' % (self.sl, self.available_slots, (self.sl / float(self.available_slots)))
        output += '<h3>OF = %.4f * %.4f - (1 - %.4f) * %.4f = %.4f (ILP obj. val = %.4f)</h3>' % (self.omega, (total_arr / float(total_x)), self.omega, (self.sl / float(self.available_slots)), (self.omega*(total_arr / float(total_x)) - (1 - self.omega) * (self.sl / float(self.available_slots))), self.obj_val)
        output += '</body></html>'

        name = 'visualization-%s.html' % suffix
        with open(name, "w") as html_file:
            html_file.write(output)

def main():
    slotframe_size = 11
    nr_frequencies = 16
    nodes = [0, 1, 2, 3]
    viz = Visualization(slotframe_size, nr_frequencies, nodes)

    viz.add_sigma(5, 2, 1, 3)
    viz.add_sigma(7, 2, 1, 3)
    viz.add_beta(2, 'QPSK_FEC_1_2', 1)
    viz.visualize()

if __name__ == "__main__":
    main()