from fileinput import filename
import sys
from components import network as nw
from components.component import Component
from components.fibre import Fibre
from components.detector import Detector 
from components.source import Source
from presets.single_link import SingleLink
from presets.repeater_chain_link import RepeaterChain
from PySide6.QtWidgets import QTreeWidget, QTreeWidgetItem, QTableWidget, QTableWidgetItem, QDialog
from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtGui import QPixmap
import numpy as np
import os.path

import matplotlib.pyplot as plt



# this file is the brain of the program, it connects all the backend logic to the GUI and calls backend classes like components and networks

class SlotHandler:
    def __init__(self, window, app_ref):
        self.window = window
        self.app_ref = app_ref
        self.network_file_open = False
        self.network = None


    #To do: make it for general label
    # def change_label(self, text):
    #     self.ui.label.setText(text)

    ### MENU BAR BTNS ###

    def exit_app(self):
        sys.exit(0)

    ### TOOLBAR BTNS ###   

    def new_button_clicked(self):
        if self.network_file_open:
            print("Network file is already open. Please close it before creating a new one.")
        else:
            print("New button clicked")
            self.network = nw.Network(name="Untitled Network")
            self.network_file_open = True
            self.tree_network = QTreeWidgetItem()
            self.tree_network.setText(0, "Untitled Network")
            self.window.componentTree.addTopLevelItem(self.tree_network)

    def run_button_clicked(self):
        print("Run button clicked")
        if self.network is not None:
            if self.network == "single_link":
                self.app_ref.show_single_link_dialog()
                

            elif self.network == "single_link_ss":
                self.app_ref.show_single_link_dialog()
        else:
            print("No network is open. Please create or open a network first.")

    def close_button_clicked(self):
        print("Close button clicked")
        if self.network_file_open:
            self.network = None
            self.network_file_open = False
            self.window.componentTree.clear()
            self.window.paramTable.clear()
            self.window.paramTable.setRowCount(0)
            self.window.paramTable.setColumnCount(0)
            
            self.window.selectedComponentLabel.setText("No component selected")
            self.window.diagramLabel.clear()
            print("Network closed.")
        else:
            print("No network is open to close.")

    def component_tree_item_clicked_handler(self, item, column):
        if self.network == "single_link":
            self.show_SL_component_param(item, column)
        elif self.network == "single_link_ss":
            self.show_SLSS_component_param(item, column)
        elif self.network == "repeater_chain":
            self.show_RC_component_param(item, column)

    def param_table_cell_changed_handler(self, row, column):
        if self.network == "single_link":
            self.SL_param_table_cell_changed(row, column)
        elif self.network == "single_link_ss":
            self.SLSS_param_table_cell_changed(row, column)
        elif self.network == "repeater_chain":
            self.RC_param_table_cell_changed(row, column)

    def single_link_dialog_handler(self):
        if self.network == "single_link":
            self.single_link_dialog_accepted()
        elif self.network == "single_link_ss":
            self.single_link_SS_dialog_accepted()

    #####################################################################  
    ####################### single link sim  ############################
    #####################################################################

    def add_single_link_button_clicked(self):
        print("Add Single Link button clicked")
        if self.network is not None:
            print("Can't add a single link to a network. Close current network and click add single link again.")
        else:
            CURRENT_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
            filename = os.path.join(CURRENT_DIRECTORY, "res", "img", "single_link_midpoint_def.png")
            self.window.diagramLabel.setPixmap(QPixmap(filename))
            self.window.diagramLabel.setScaledContents(True)
            print(filename)
            print("Looking for image at:", filename)
            print("Exists?", os.path.exists(filename))

            # self.single_link = SingleLink(l=1, mu=1, alpha=1, det_1_eff=1, det_2_eff=1,
            #            prob_dc_per_freq_per_bin_det_1=0, prob_dc_per_freq_per_bin_det_2=0,
            #            verbose=False, detector_type='guha', source_rep_rate=1, arch='midpoint')
            self.network = "single_link"
            self.single_link_open = True
            self.network_file_open = True
            self.tree_single_link = QTreeWidgetItem()
            self.tree_single_link.setText(0, "Single Link")
            self.window.componentTree.addTopLevelItem(self.tree_single_link)
            self.tree_single_link_source = QTreeWidgetItem()
            self.tree_single_link_source.setText(0, "Midpoint Source")
            self.tree_single_link.addChild(self.tree_single_link_source)
            for i in range(2):
                self.tree_single_link_detector = QTreeWidgetItem()
                self.tree_single_link_detector.setText(0, "Detector {}".format(i + 1))
                self.tree_single_link.addChild(self.tree_single_link_detector)
            self.tree_single_link.setExpanded(True)

            self.selected_comp = None

            # component params

            global single_link_src_params
            single_link_src_params = {
                "mu": 0,
                "source_rep_rate": 0,
            }
            global single_link_det_1_params
            single_link_det_1_params = {
                "det_1_eff": 0,
                "prob_dc_per_freq_per_bin_det_1": 0,
            }
            global single_link_det_2_params
            single_link_det_2_params = {
                "det_2_eff": 0,
                "prob_dc_per_freq_per_bin_det_2": 0,
            }

    def SL_srcRepRateRBtn_selected(self):
        self.app_ref.SL_indVar = 0
        self.ind_var_name = "Source Repetition Rate (MHz)"

    def SL_dcProbPerBinRBtn_selected(self):
        self.app_ref.SL_indVar = 1
        self.ind_var_name = "Detector Dark Count Probability"

    def SL_detEffRBtn_selected(self):
        self.app_ref.SL_indVar = 2
        self.ind_var_name = "Detector Efficiency"

    def SL_linkLengthRBtn_selected(self):
        self.app_ref.SL_indVar = 3
        self.ind_var_name = "Link Length (km)"

    def SL_entProbRBtn_selected(self):
        self.app_ref.SL_depVar = 0
        self.dep_var_name = "Entanglement Probability"

    def SL_entRateRBtn_selected(self):
        self.app_ref.SL_depVar = 1
        self.dep_var_name = "Entanglement Rate"

    def SL_entFidRBtn_selected(self):
        self.app_ref.SL_depVar = 2
        self.dep_var_name = "Entanglement Fidelity F"
    
    def show_SL_component_param(self, item, column):
        self.window.paramTable.blockSignals(True)
        self.window.paramTable.setRowCount(2)
        self.window.paramTable.setColumnCount(3)
        self.window.paramTable.setHorizontalHeaderLabels(["Parameter", "Value", "Units"])
        self.window.paramTable.resizeColumnsToContents()
        if item.text(0) == "Midpoint Source":
            print("Source parameters:")
            for param, value in single_link_src_params.items():
                print("  {}: {}".format(param, value))

            self.window.selectedComponentLabel.setText("Midpoint Source")
            self.window.paramTable.setItem(0, 0, QTableWidgetItem("μ"))
            self.window.paramTable.setItem(0, 1, QTableWidgetItem(str(single_link_src_params["mu"])))
            self.window.paramTable.setItem(0, 2, QTableWidgetItem("photons/qubit"))

            self.window.paramTable.setItem(1, 0, QTableWidgetItem("Repetition rate"))
            self.window.paramTable.setItem(1, 1, QTableWidgetItem(str(single_link_src_params["source_rep_rate"])))
            self.window.paramTable.setItem(1, 2, QTableWidgetItem("MHz"))

            self.selected_comp = "Source"
            self.window.paramTable.resizeColumnsToContents()

        if item.text(0) == "Detector 1":
            print("Detector 1 parameters:")
            for param, value in single_link_det_1_params.items():
                print("  {}: {}".format(param, value))

            self.window.selectedComponentLabel.setText("Detector 1")
            self.window.paramTable.setItem(0, 0, QTableWidgetItem("Efficiency"))
            self.window.paramTable.setItem(0, 1, QTableWidgetItem(str(single_link_det_1_params["det_1_eff"])))
            self.window.paramTable.setItem(0, 2, QTableWidgetItem(""))

            self.window.paramTable.setItem(1, 0, QTableWidgetItem("P(dark count/freq. bin)"))
            self.window.paramTable.setItem(1, 1, QTableWidgetItem(str(single_link_det_1_params["prob_dc_per_freq_per_bin_det_1"])))
            self.window.paramTable.setItem(1, 2, QTableWidgetItem(""))

            self.selected_comp = "Detector 1"
            self.window.paramTable.resizeColumnsToContents()

        if item.text(0) == "Detector 2":
            print("Detector 2 parameters:")
            for param, value in single_link_det_2_params.items():
                print("  {}: {}".format(param, value))

            self.window.selectedComponentLabel.setText("Detector 2")
            self.window.paramTable.setItem(0, 0, QTableWidgetItem("Efficiency"))
            self.window.paramTable.setItem(0, 1, QTableWidgetItem(str(single_link_det_2_params["det_2_eff"])))
            self.window.paramTable.setItem(0, 2, QTableWidgetItem(""))

            self.window.paramTable.setItem(1, 0, QTableWidgetItem("P(dark count/ freq. bin)"))
            self.window.paramTable.setItem(1, 1, QTableWidgetItem(str(single_link_det_2_params["prob_dc_per_freq_per_bin_det_2"])))
            self.window.paramTable.setItem(1, 2, QTableWidgetItem(""))

            self.selected_comp = "Detector 2"
            self.window.paramTable.resizeColumnsToContents()
        self.window.paramTable.blockSignals(False)

    def SL_param_table_cell_changed(self, row, column):

        print(single_link_src_params, single_link_det_1_params, single_link_det_2_params)
        self.window.paramTable.resizeColumnsToContents()
        if row == 0 and column == 1:
            new_value = self.window.paramTable.item(row, column).text()
            if self.selected_comp == "Source":
                single_link_src_params["mu"] = float(new_value)
                print("Updated Source mu to", new_value)
            elif self.selected_comp == "Detector 1":
                single_link_det_1_params["det_1_eff"] = float(new_value)
                print("Updated Detector 1 efficiency to", new_value)
            elif self.selected_comp == "Detector 2":
                single_link_det_2_params["det_2_eff"] = float(new_value)
                print("Updated Detector 2 efficiency to", new_value)
        if row == 1 and column == 1:
            new_value = self.window.paramTable.item(row, column).text()
            if self.selected_comp == "Source":
                single_link_src_params["source_rep_rate"] = float(new_value)
                print("Updated Source repetition rate to", new_value)
            elif self.selected_comp == "Detector 1":
                single_link_det_1_params["prob_dc_per_freq_per_bin_det_1"] = float(new_value)
                print("Updated Detector 1 dark count probability to", new_value)
            elif self.selected_comp == "Detector 2":
                single_link_det_2_params["prob_dc_per_freq_per_bin_det_2"] = float(new_value)
                print("Updated Detector 2 dark count probability to", new_value)
        



    def single_link_dialog_accepted(self):
        self.app_ref.close_single_link_dialog()
        if self.app_ref.SL_indVar == 0:
            srcRepRate_range = self.app_ref.get_src_rep_rate_range()
            dcProb_range = [single_link_det_1_params["prob_dc_per_freq_per_bin_det_1"], single_link_det_1_params["prob_dc_per_freq_per_bin_det_1"]]
            defEff_range = [single_link_det_1_params["det_1_eff"], single_link_det_1_params["det_1_eff"]]
            length_range = [1000, 1000]
           # print(self.single_link_src_params["mu"])
            
        elif self.app_ref.SL_indVar == 1:
            dcProb_range = self.app_ref.get_dc_prob_range()
            defEff_range = [single_link_det_1_params["det_1_eff"], single_link_det_2_params["det_2_eff"]]
            length_range = [1000, 1000]
            srcRepRate_range = [single_link_src_params["source_rep_rate"], single_link_src_params["source_rep_rate"]]

        elif self.app_ref.SL_indVar == 2:
            defEff_range = self.app_ref.get_def_eff_range()
            srcRepRate_range = [single_link_src_params["source_rep_rate"], single_link_src_params["source_rep_rate"]]
            dcProb_range = [single_link_det_1_params["prob_dc_per_freq_per_bin_det_1"], single_link_det_1_params["prob_dc_per_freq_per_bin_det_1"]]
            length_range = [1000, 1000]

        elif self.app_ref.SL_indVar == 3:
            length_range = self.app_ref.get_len_range()
            srcRepRate_range = [single_link_src_params["source_rep_rate"], single_link_src_params["source_rep_rate"]]
            dcProb_range = [single_link_det_1_params["prob_dc_per_freq_per_bin_det_1"], single_link_det_1_params["prob_dc_per_freq_per_bin_det_1"]]
            defEff_range = [single_link_det_1_params["det_1_eff"], single_link_det_2_params["det_2_eff"]]

        atten = self.app_ref.get_atten()

        iterations = self.app_ref.get_iterations()
        ind_vars = np.array([np.linspace(srcRepRate_range[0], srcRepRate_range[1], iterations),
                            np.linspace(dcProb_range[0], dcProb_range[1], iterations),
                            np.linspace(defEff_range[0], defEff_range[1], iterations),
                            np.linspace(length_range[0], length_range[1], iterations)])
        dep_vars = np.empty([3, iterations])
        fidelity = []
        
        length = np.linspace(length_range[0], length_range[1], iterations)
        print(ind_vars)
        plt.figure(figsize=(10, 5))
        for i in range(iterations):
            print(ind_vars[2, i], ind_vars[0, i], ind_vars[1, i], ind_vars[3, i])
            self.single_link = SingleLink(l=ind_vars[3, i], mu=.2, alpha=atten, det_1_eff=ind_vars[2, i], det_2_eff=ind_vars[2, i],
            prob_dc_per_freq_per_bin_det_1=ind_vars[1, i], prob_dc_per_freq_per_bin_det_2=ind_vars[1, i],
            verbose=False, detector_type='guha', source_rep_rate=ind_vars[0, i], arch='midpoint')
            a_e_plus_b_e, source_rep_rate_times_a_e_plus_b_e, fid = self.single_link.run()
            # here: create numpy array of all results and instead of just appending fid as here add all results
            # then plot results based on ind/dep var index selection
            dep_vars[0, i] = a_e_plus_b_e
            dep_vars[1, i] = source_rep_rate_times_a_e_plus_b_e
            dep_vars[2, i] = fid
        plt.plot(ind_vars[self.app_ref.SL_indVar], dep_vars[self.app_ref.SL_depVar], label='Guha', color='blue')
        
        for i in range(iterations):
            print(ind_vars[2, i], ind_vars[0, i], ind_vars[1, i], ind_vars[3, i])
            self.single_link = SingleLink(l=ind_vars[3, i], mu=.2, alpha=atten, det_1_eff=ind_vars[2, i], det_2_eff=ind_vars[2, i],
            prob_dc_per_freq_per_bin_det_1=ind_vars[1, i], prob_dc_per_freq_per_bin_det_2=ind_vars[1, i],
            verbose=False, detector_type='PNR', source_rep_rate=ind_vars[0, i], arch='midpoint')
            a_e_plus_b_e, source_rep_rate_times_a_e_plus_b_e, fid = self.single_link.run()
            # here: create numpy array of all results and instead of just appending fid as here add all results
            # then plot results based on ind/dep var index selection
            dep_vars[0, i] = a_e_plus_b_e
            dep_vars[1, i] = source_rep_rate_times_a_e_plus_b_e
            dep_vars[2, i] = fid
        plt.plot(ind_vars[self.app_ref.SL_indVar], dep_vars[self.app_ref.SL_depVar], label='PNR', color='red')
        
        for i in range(iterations):
            print(ind_vars[2, i], ind_vars[0, i], ind_vars[1, i], ind_vars[3, i])
            self.single_link = SingleLink(l=ind_vars[3, i], mu=0.2, alpha=atten, det_1_eff=ind_vars[2, i], det_2_eff=ind_vars[2, i],
            prob_dc_per_freq_per_bin_det_1=ind_vars[1, i], prob_dc_per_freq_per_bin_det_2=ind_vars[1, i],
            verbose=False, detector_type='non_PNR', source_rep_rate=ind_vars[0, i], arch='midpoint')
            a_e_plus_b_e, source_rep_rate_times_a_e_plus_b_e, fid = self.single_link.run()
            # here: create numpy array of all results and instead of just appending fid as here add all results
            # then plot results based on ind/dep var index selection
            dep_vars[0, i] = a_e_plus_b_e
            dep_vars[1, i] = source_rep_rate_times_a_e_plus_b_e
            dep_vars[2, i] = fid
        plt.plot(ind_vars[self.app_ref.SL_indVar], dep_vars[self.app_ref.SL_depVar], label='non - PNR', color='green')

        print(self.app_ref.SL_depVar, self.app_ref.SL_indVar)
        
        
        print(ind_vars[self.app_ref.SL_indVar], dep_vars[self.app_ref.SL_depVar])
        plt.xlabel(self.ind_var_name)
        plt.ylabel(self.dep_var_name)
        plt.grid(True)
        plt.legend()
        plt.show()
        print(self.app_ref.SL_indVar)

    def stop_button_clicked(self):
        print("Stop button clicked")

    def save_button_clicked(self, text):
        print(text)

    #####################################################################  
    #################### single link src at sender ######################
    #####################################################################

    def add_single_link_button_src_at_sender_clicked(self):
        print("Add Single Link button clicked")
        if self.network is not None:
            print("Can't add a single link to a network. Close current network and click add single link again.")
        else:
            CURRENT_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
            filename = os.path.join(CURRENT_DIRECTORY, "res", "img", "single_link_src_at_sender_def.png")
            self.window.diagramLabel.setPixmap(QPixmap(filename))
           # self.window.diagramLabel.setScaledContents(True)
            print(filename)
            print("Looking for image at:", filename)
            print("Exists?", os.path.exists(filename))

            # self.single_link = SingleLink(l=1, mu=1, alpha=1, det_1_eff=1, det_2_eff=1,
            #            prob_dc_per_freq_per_bin_det_1=0, prob_dc_per_freq_per_bin_det_2=0,
            #            verbose=False, detector_type='guha', source_rep_rate=1, arch='midpoint')
            self.network = "single_link_ss"
            self.single_link_open = True
            self.network_file_open = True
            self.tree_single_link = QTreeWidgetItem()
            self.tree_single_link.setText(0, "Single Link")
            self.window.componentTree.addTopLevelItem(self.tree_single_link)
            self.tree_single_link_source = QTreeWidgetItem()
            self.tree_single_link_source.setText(0, "Source at Sender")
            self.tree_single_link.addChild(self.tree_single_link_source)
            for i in range(2):
                self.tree_single_link_detector = QTreeWidgetItem()
                self.tree_single_link_detector.setText(0, "Detector {}".format(i + 1))
                self.tree_single_link.addChild(self.tree_single_link_detector)
            self.tree_single_link.setExpanded(True)

            self.selected_comp = None

            # component params

            global single_link_ss_src_params
            single_link_ss_src_params = {
                "mu": 0,
                "source_rep_rate": 0,
            }
            global single_link_ss_det_1_params
            single_link_ss_det_1_params = {
                "det_1_eff": 0,
                "prob_dc_per_freq_per_bin_det_1": 0,
            }
            global single_link_ss_det_2_params
            single_link_ss_det_2_params = {
                "det_2_eff": 0,
                "prob_dc_per_freq_per_bin_det_2": 0,
            }

    def SLSS_srcRepRateRBtn_selected(self):
        self.app_ref.SL_indVar = 0
        self.ind_var_name = "Source Repetition Rate (MHz)"

    def SLSS_dcProbPerBinRBtn_selected(self):
        self.app_ref.SL_indVar = 1
        self.ind_var_name = "Detector Dark Count Probability"

    def SLSS_detEffRBtn_selected(self):
        self.app_ref.SL_indVar = 2
        self.ind_var_name = "Detector Efficiency"

    def SLSS_linkLengthRBtn_selected(self):
        self.app_ref.SL_indVar = 3
        self.ind_var_name = "Link Length (km)"

    def SLSS_entProbRBtn_selected(self):
        self.app_ref.SL_depVar = 0
        self.dep_var_name = "Entanglement Probability"

    def SLSS_entRateRBtn_selected(self):
        self.app_ref.SL_depVar = 1
        self.dep_var_name = "Entanglement Rate"

    def SLSS_entFidRBtn_selected(self):
        self.app_ref.SL_depVar = 2
        self.dep_var_name = "Entanglement Fidelity F"
    
    def show_SLSS_component_param(self, item, column):
        self.window.paramTable.blockSignals(True)
        self.window.paramTable.setRowCount(2)
        self.window.paramTable.setColumnCount(3)
        self.window.paramTable.setHorizontalHeaderLabels(["Parameter", "Value", "Units"])
        self.window.paramTable.resizeColumnsToContents()
        if item.text(0) == "Source at Sender":
            print("Source parameters:")
            for param, value in single_link_ss_src_params.items():
                print("  {}: {}".format(param, value))

            self.window.selectedComponentLabel.setText("Source at Sender")
            self.window.paramTable.setItem(0, 0, QTableWidgetItem("μ"))
            self.window.paramTable.setItem(0, 1, QTableWidgetItem(str(single_link_ss_src_params["mu"])))
            self.window.paramTable.setItem(0, 2, QTableWidgetItem("photons/qubit"))

            self.window.paramTable.setItem(1, 0, QTableWidgetItem("Repetition rate"))
            self.window.paramTable.setItem(1, 1, QTableWidgetItem(str(single_link_ss_src_params["source_rep_rate"])))
            self.window.paramTable.setItem(1, 2, QTableWidgetItem("MHz"))

            self.selected_comp = "Source"
            self.window.paramTable.resizeColumnsToContents()

        if item.text(0) == "Detector 1":
            print("Detector 1 parameters:")
            for param, value in single_link_det_1_params.items():
                print("  {}: {}".format(param, value))

            self.window.selectedComponentLabel.setText("Detector 1")
            self.window.paramTable.setItem(0, 0, QTableWidgetItem("Efficiency"))
            self.window.paramTable.setItem(0, 1, QTableWidgetItem(str(single_link_ss_det_1_params["det_1_eff"])))
            self.window.paramTable.setItem(0, 2, QTableWidgetItem(""))

            self.window.paramTable.setItem(1, 0, QTableWidgetItem("P(dark count/freq. bin)"))
            self.window.paramTable.setItem(1, 1, QTableWidgetItem(str(single_link_ss_det_1_params["prob_dc_per_freq_per_bin_det_1"])))
            self.window.paramTable.setItem(1, 2, QTableWidgetItem(""))

            self.selected_comp = "Detector 1"
            self.window.paramTable.resizeColumnsToContents()

        if item.text(0) == "Detector 2":
            print("Detector 2 parameters:")
            for param, value in single_link_ss_det_2_params.items():
                print("  {}: {}".format(param, value))

            self.window.selectedComponentLabel.setText("Detector 2")
            self.window.paramTable.setItem(0, 0, QTableWidgetItem("Efficiency"))
            self.window.paramTable.setItem(0, 1, QTableWidgetItem(str(single_link_ss_det_2_params["det_2_eff"])))
            self.window.paramTable.setItem(0, 2, QTableWidgetItem(""))

            self.window.paramTable.setItem(1, 0, QTableWidgetItem("P(dark count/ freq. bin)"))
            self.window.paramTable.setItem(1, 1, QTableWidgetItem(str(single_link_ss_det_2_params["prob_dc_per_freq_per_bin_det_2"])))
            self.window.paramTable.setItem(1, 2, QTableWidgetItem(""))

            self.selected_comp = "Detector 2"
            self.window.paramTable.resizeColumnsToContents()
        self.window.paramTable.blockSignals(False)

    def SLSS_param_table_cell_changed(self, row, column):

        print(single_link_ss_src_params, single_link_ss_det_1_params, single_link_ss_det_2_params)
        self.window.paramTable.resizeColumnsToContents()
        if row == 0 and column == 1:
            new_value = self.window.paramTable.item(row, column).text()
            if self.selected_comp == "Source":
                single_link_ss_src_params["mu"] = float(new_value)
                print("Updated Source mu to", new_value)
            elif self.selected_comp == "Detector 1":
                single_link_ss_det_1_params["det_1_eff"] = float(new_value)
                print("Updated Detector 1 efficiency to", new_value)
            elif self.selected_comp == "Detector 2":
                single_link_ss_det_2_params["det_2_eff"] = float(new_value)
                print("Updated Detector 2 efficiency to", new_value)
        if row == 1 and column == 1:
            new_value = self.window.paramTable.item(row, column).text()
            if self.selected_comp == "Source":
                single_link_ss_src_params["source_rep_rate"] = float(new_value)
                print("Updated Source repetition rate to", new_value)
            elif self.selected_comp == "Detector 1":
                single_link_ss_det_1_params["prob_dc_per_freq_per_bin_det_1"] = float(new_value)
                print("Updated Detector 1 dark count probability to", new_value)
            elif self.selected_comp == "Detector 2":
                single_link_ss_det_2_params["prob_dc_per_freq_per_bin_det_2"] = float(new_value)
                print("Updated Detector 2 dark count probability to", new_value)
        



    def single_link_SS_dialog_accepted(self):
        self.app_ref.close_single_link_dialog()
        if self.app_ref.SL_indVar == 0:
            srcRepRate_range = self.app_ref.get_src_rep_rate_range()
            dcProb_range = [single_link_ss_det_1_params["prob_dc_per_freq_per_bin_det_1"], single_link_ss_det_1_params["prob_dc_per_freq_per_bin_det_1"]]
            defEff_range = [single_link_ss_det_1_params["det_1_eff"], single_link_ss_det_1_params["det_1_eff"]]
            length_range = [1000, 1000]
           # print(self.single_link_src_params["mu"])
            
        elif self.app_ref.SL_indVar == 1:
            dcProb_range = self.app_ref.get_dc_prob_range()
            defEff_range = [single_link_ss_det_1_params["det_1_eff"], single_link_ss_det_2_params["det_2_eff"]]
            length_range = [1000, 1000]
            srcRepRate_range = [single_link_ss_src_params["source_rep_rate"], single_link_ss_src_params["source_rep_rate"]]

        elif self.app_ref.SL_indVar == 2:
            defEff_range = self.app_ref.get_def_eff_range()
            srcRepRate_range = [single_link_ss_src_params["source_rep_rate"], single_link_ss_src_params["source_rep_rate"]]
            dcProb_range = [single_link_ss_det_1_params["prob_dc_per_freq_per_bin_det_1"], single_link_ss_det_1_params["prob_dc_per_freq_per_bin_det_1"]]
            length_range = [1000, 1000]

        elif self.app_ref.SL_indVar == 3:
            length_range = self.app_ref.get_len_range()
            srcRepRate_range = [single_link_ss_src_params["source_rep_rate"], single_link_ss_src_params["source_rep_rate"]]
            dcProb_range = [single_link_ss_det_1_params["prob_dc_per_freq_per_bin_det_1"], single_link_ss_det_1_params["prob_dc_per_freq_per_bin_det_1"]]
            defEff_range = [single_link_ss_det_1_params["det_1_eff"], single_link_ss_det_2_params["det_2_eff"]]

        atten = self.app_ref.get_atten()

        iterations = self.app_ref.get_iterations()
        ind_vars = np.array([np.linspace(srcRepRate_range[0], srcRepRate_range[1], iterations),
                            np.linspace(dcProb_range[0], dcProb_range[1], iterations),
                            np.linspace(defEff_range[0], defEff_range[1], iterations),
                            np.linspace(length_range[0], length_range[1], iterations)])
        dep_vars = np.empty([3, iterations])
        fidelity = []
        
        length = np.linspace(length_range[0], length_range[1], iterations)
        print(ind_vars)
        plt.figure(figsize=(10, 5))
        for i in range(iterations):
            print(ind_vars[2, i], ind_vars[0, i], ind_vars[1, i], ind_vars[3, i])
            self.single_link = SingleLink(l=ind_vars[3, i], mu=.2, alpha=atten, det_1_eff=ind_vars[2, i], det_2_eff=ind_vars[2, i],
            prob_dc_per_freq_per_bin_det_1=ind_vars[1, i], prob_dc_per_freq_per_bin_det_2=ind_vars[1, i],
            verbose=False, detector_type='guha', source_rep_rate=ind_vars[0, i], arch='source_at_sender')
            a_e_plus_b_e, source_rep_rate_times_a_e_plus_b_e, fid = self.single_link.run()
            # here: create numpy array of all results and instead of just appending fid as here add all results
            # then plot results based on ind/dep var index selection
            dep_vars[0, i] = a_e_plus_b_e
            dep_vars[1, i] = source_rep_rate_times_a_e_plus_b_e
            dep_vars[2, i] = fid
        plt.plot(ind_vars[self.app_ref.SL_indVar], dep_vars[self.app_ref.SL_depVar], label='Guha', color='blue')
        
        for i in range(iterations):
            print(ind_vars[2, i], ind_vars[0, i], ind_vars[1, i], ind_vars[3, i])
            self.single_link = SingleLink(l=ind_vars[3, i], mu=.2, alpha=atten, det_1_eff=ind_vars[2, i], det_2_eff=ind_vars[2, i],
            prob_dc_per_freq_per_bin_det_1=ind_vars[1, i], prob_dc_per_freq_per_bin_det_2=ind_vars[1, i],
            verbose=False, detector_type='PNR', source_rep_rate=ind_vars[0, i], arch='source_at_sender')
            a_e_plus_b_e, source_rep_rate_times_a_e_plus_b_e, fid = self.single_link.run()
            # here: create numpy array of all results and instead of just appending fid as here add all results
            # then plot results based on ind/dep var index selection
            dep_vars[0, i] = a_e_plus_b_e
            dep_vars[1, i] = source_rep_rate_times_a_e_plus_b_e
            dep_vars[2, i] = fid
        plt.plot(ind_vars[self.app_ref.SL_indVar], dep_vars[self.app_ref.SL_depVar], label='PNR', color='red')
        
        for i in range(iterations):
            print(ind_vars[2, i], ind_vars[0, i], ind_vars[1, i], ind_vars[3, i])
            self.single_link = SingleLink(l=ind_vars[3, i], mu=0.2, alpha=atten, det_1_eff=ind_vars[2, i], det_2_eff=ind_vars[2, i],
            prob_dc_per_freq_per_bin_det_1=ind_vars[1, i], prob_dc_per_freq_per_bin_det_2=ind_vars[1, i],
            verbose=False, detector_type='non_PNR', source_rep_rate=ind_vars[0, i], arch='source_at_sender')
            a_e_plus_b_e, source_rep_rate_times_a_e_plus_b_e, fid = self.single_link.run()
            # here: create numpy array of all results and instead of just appending fid as here add all results
            # then plot results based on ind/dep var index selection
            dep_vars[0, i] = a_e_plus_b_e
            dep_vars[1, i] = source_rep_rate_times_a_e_plus_b_e
            dep_vars[2, i] = fid
        plt.plot(ind_vars[self.app_ref.SL_indVar], dep_vars[self.app_ref.SL_depVar], label='non - PNR', color='green')

        print(self.app_ref.SL_depVar, self.app_ref.SL_indVar)
        
        
        print(ind_vars[self.app_ref.SL_indVar], dep_vars[self.app_ref.SL_depVar])
        plt.xlabel(self.ind_var_name)
        plt.ylabel(self.dep_var_name)
        plt.grid(True)
        plt.title("Source at Sender")
        plt.legend()
        plt.show()
        print(self.app_ref.SL_indVar)

    def stop_button_clicked(self):
        print("Stop button clicked")

    def save_button_clicked(self, text):
        print(text)

    def add_repeater_chain_button_clicked(self):
        print("Add Repeater Chain button clicked")
        if self.network is not None:
            print("Can't add a repeater chain to a network. Close current network and click add repeater chain again.")
        else:
            self.network = "repeater_chain"
    ### COMPONENTS BTNS ###

    def add_source_button_clicked(self):
        print("Add Source button clicked")
        if self.network is not None:
            Source(network=self.network, name="Source {}".format(len(self.network.sources)))
            self.tree_source = QTreeWidgetItem()
            self.tree_source.setText(0, "Source {}".format(len(self.network.sources)))
            self.tree_network.addChild(self.tree_source)
            self.tree_network.setExpanded(True)
        else:
            print("No network is open. Please create or open a network first.")

    def add_detector_button_clicked(self):
        print("Add Detector button clicked")
        if self.network is not None:
            Detector(network=self.network, name="Detector {}".format(len(self.network.detectors)))
            self.tree_detector = QTreeWidgetItem()
            self.tree_detector.setText(0, "Detector {}".format(len(self.network.detectors)))
            self.tree_network.addChild(self.tree_detector)
            self.tree_network.setExpanded(True)
        else:
            print("No network is open. Please create or open a network first.")

    def add_fibre_button_clicked(self):
        print("Add Fibre button clicked")


    #####################################################################  
    ########################## repeater chain ###########################
    #####################################################################

    def add_repeater_chain_button_clicked(self):
        print("Add Repeater Chain button clicked")
        if self.network is not None:
            print("Can't add a single link to a network. Close current network and click add single link again.")
        else:
            self.network_file_open = True
            CURRENT_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
            filename = os.path.join(CURRENT_DIRECTORY, "res", "img", "repeater_chain.png")
            self.window.diagramLabel.setPixmap(QPixmap(filename))
            self.window.diagramLabel.setScaledContents(True)
            print(filename)
            print("Looking for image at:", filename)
            print("Exists?", os.path.exists(filename))

            # self.single_link = SingleLink(l=1, mu=1, alpha=1, det_1_eff=1, det_2_eff=1,
            #            prob_dc_per_freq_per_bin_det_1=0, prob_dc_per_freq_per_bin_det_2=0,
            #            verbose=False, detector_type='guha', source_rep_rate=1, arch='midpoint')
            self.network = "repeater_chain"
            self.repeater_chain_open = True
            self.tree_repeater_chain = QTreeWidgetItem()
            self.tree_repeater_chain.setText(0, "Repeater Chain")
            self.window.componentTree.addTopLevelItem(self.tree_repeater_chain)
            self.tree_repeater_chain_source = QTreeWidgetItem()
            self.tree_repeater_chain_source.setText(0, "Elementary Link")
            self.tree_repeater_chain.addChild(self.tree_repeater_chain_source)
            self.tree_repeater_chain_detector = QTreeWidgetItem()
            self.tree_repeater_chain_detector.setText(0, "Repeater Node")
            self.tree_repeater_chain.addChild(self.tree_repeater_chain_detector)
            self.tree_repeater_chain.setExpanded(True)

            self.selected_comp = None

            # component params

            global repeater_chain_EL_params
            repeater_chain_EL_params = {
                "bsm_det_1_eff": 0,
                "bsm_det_2_eff": 0,
                "prob_dc_per_freq_per_bin_per_freq": 0,
                "source_rep_rate": 0,
                "qm_loading_eff": 0,
                "qm_emitting_eff": 0,
            }
            global repeater_chain_RN_params
            repeater_chain_RN_params = {
                "bsm_det_1_eff": 0,
                "bsm_det_2_eff": 0,
                "prob_dc_per_bin_per_freq": 0,
            }

    def show_RC_component_param(self, item, column):
        self.window.paramTable.blockSignals(True)
        self.window.paramTable.setRowCount(0)
        self.window.paramTable.setColumnCount(0)

        self.window.paramTable.resizeColumnsToContents()
        if item.text(0) == "Elementary Link":
            print("Elementary Link parameters:")
            for param, value in repeater_chain_EL_params.items():
                print("  {}: {}".format(param, value))

            self.window.paramTable.setRowCount(6)
            self.window.paramTable.setColumnCount(3)
            self.window.paramTable.setHorizontalHeaderLabels(["Parameter", "Value", "Units"])

            self.window.selectedComponentLabel.setText("Elementary Link")
            self.window.paramTable.setItem(0, 0, QTableWidgetItem("BSM detector 1 efficiency"))
            self.window.paramTable.setItem(0, 1, QTableWidgetItem(str(repeater_chain_EL_params["bsm_det_1_eff"])))
            self.window.paramTable.setItem(0, 2, QTableWidgetItem(""))

            self.window.paramTable.setItem(1, 0, QTableWidgetItem("BSM detector 2 efficiency"))
            self.window.paramTable.setItem(1, 1, QTableWidgetItem(str(repeater_chain_EL_params["bsm_det_2_eff"])))
            self.window.paramTable.setItem(1, 2, QTableWidgetItem(""))

            self.window.paramTable.setItem(2, 0, QTableWidgetItem("P(dark count/freq. bin)"))
            self.window.paramTable.setItem(2, 1, QTableWidgetItem(str(repeater_chain_EL_params["prob_dc_per_freq_per_bin_per_freq"])))
            self.window.paramTable.setItem(2, 2, QTableWidgetItem(""))

            self.window.paramTable.setItem(3, 0, QTableWidgetItem("Source repetition rate"))
            self.window.paramTable.setItem(3, 1, QTableWidgetItem(str(repeater_chain_EL_params["source_rep_rate"])))
            self.window.paramTable.setItem(3, 2, QTableWidgetItem("MHz"))

            self.window.paramTable.setItem(4, 0, QTableWidgetItem("QM loading efficiency"))
            self.window.paramTable.setItem(4, 1, QTableWidgetItem(str(repeater_chain_EL_params["qm_loading_eff"])))
            self.window.paramTable.setItem(4, 2, QTableWidgetItem(""))

            self.window.paramTable.setItem(5, 0, QTableWidgetItem("QM emitting efficiency"))
            self.window.paramTable.setItem(5, 1, QTableWidgetItem(str(repeater_chain_EL_params["qm_emitting_eff"])))
            self.window.paramTable.setItem(5, 2, QTableWidgetItem(""))

            self.selected_comp = "Elementary Link"
            self.window.paramTable.resizeColumnsToContents()

        if item.text(0) == "Repeater Node":
            print("Repeater Node parameters:")
            for param, value in repeater_chain_RN_params.items():
                print("  {}: {}".format(param, value))

            self.window.paramTable.setRowCount(3)
            self.window.paramTable.setColumnCount(3)
            self.window.paramTable.setHorizontalHeaderLabels(["Parameter", "Value", "Units"])

            self.window.selectedComponentLabel.setText("Repeater Node")
            self.window.paramTable.setItem(0, 0, QTableWidgetItem("BSM detector 1 efficiency"))
            self.window.paramTable.setItem(0, 1, QTableWidgetItem(str(repeater_chain_RN_params["bsm_det_1_eff"])))
            self.window.paramTable.setItem(0, 2, QTableWidgetItem(""))
            
            self.window.paramTable.setItem(1, 0, QTableWidgetItem("BSM detector 2 efficiency"))
            self.window.paramTable.setItem(1, 1, QTableWidgetItem(str(repeater_chain_RN_params["bsm_det_2_eff"])))
            self.window.paramTable.setItem(1, 2, QTableWidgetItem(""))

            self.window.paramTable.setItem(2, 0, QTableWidgetItem("P(dark count/freq. bin)"))
            self.window.paramTable.setItem(2, 1, QTableWidgetItem(str(repeater_chain_RN_params["prob_dc_per_bin_per_freq"])))
            self.window.paramTable.setItem(2, 2, QTableWidgetItem(""))

            self.selected_comp = "Repeater Node"
            self.window.paramTable.resizeColumnsToContents()

        self.window.paramTable.blockSignals(False)

    def RC_param_table_cell_changed(self, row, column):
        pass
    
    # # repeater tests with Perfect memory. only efficiency loading and emitting qubits is simulated

    # a_succ = []
    # b_succ = []
    # c_succ = []

    # a_fid = []
    # b_fid = []
    # c_fid = []

    # source_rep_rate = 50 # MHz
    
    # # mess with m to show its necessary, m =1 is bad
    # m = 1000 # number of ortho frequencies
    # alpha = .2
    # eff_el_bsm_detector_1 = 1
    # eff_el_bsm_detector_2 = 1
    # P_el_dc_per_bin_per_freq = 0

    # eff_rep_bsm_detector_1 = 1
    # eff_rep_bsm_detector_2 = 1
    # P_rep_dc_per_bin_per_freq = 0
    
    # # maybe look at? but not too interesting
    # eff_loading_qm = 1
    # eff_emitting_qm = 1
    
    # # probably don't look at, cause jake does in his section
    # mu= .1
    
    # lengths = np.linspace(0, 2000, 1000)  # km

    # for l in lengths:
    #     rep_a = RepeaterChain(
    #         source_rep_rate=source_rep_rate,
    #         detector_type='PNR', # look at these
    #         l=l,
    #         m=m,
    #         alpha=alpha,
    #         eff_el_bsm_detector_1=eff_el_bsm_detector_1,
    #         eff_el_bsm_detector_2=eff_el_bsm_detector_2,
    #         P_el_dc_per_bin_per_freq=P_el_dc_per_bin_per_freq,
    #         eff_rep_bsm_detector_1=eff_rep_bsm_detector_1,
    #         eff_rep_bsm_detector_2=eff_rep_bsm_detector_2,
    #         P_rep_dc_per_bin_per_freq=P_rep_dc_per_bin_per_freq,
    #         eff_loading_qm=eff_loading_qm,
    #         eff_emitting_qm=eff_emitting_qm,
    #         mu=mu,
    #         num_elem_links=1 # and this
    #         )
    #     a_succ.append(rep_a.run()[1])
    #     a_fid.append(rep_a.run()[2])

    #     rep_a = RepeaterChain(
    #         source_rep_rate=source_rep_rate,
    #         detector_type='non_PNR',
    #         l=l,
    #         m=m,
    #         alpha=alpha,
    #         eff_el_bsm_detector_1=eff_el_bsm_detector_1,
    #         eff_el_bsm_detector_2=eff_el_bsm_detector_2,
    #         P_el_dc_per_bin_per_freq=P_el_dc_per_bin_per_freq,
    #         eff_rep_bsm_detector_1=eff_rep_bsm_detector_1,
    #         eff_rep_bsm_detector_2=eff_rep_bsm_detector_2,
    #         P_rep_dc_per_bin_per_freq=P_rep_dc_per_bin_per_freq,
    #         eff_loading_qm=eff_loading_qm,
    #         eff_emitting_qm=eff_emitting_qm,
    #         mu=mu,
    #         num_elem_links=2
    #         )
    #     b_succ.append(rep_a.run()[1])
    #     b_fid.append(rep_a.run()[2])

    #     rep_a = RepeaterChain(
    #         source_rep_rate=source_rep_rate,
    #         detector_type='guha',
    #         l=l,
    #         m=m,
    #         alpha=alpha,
    #         eff_el_bsm_detector_1=eff_el_bsm_detector_1,
    #         eff_el_bsm_detector_2=eff_el_bsm_detector_2,
    #         P_el_dc_per_bin_per_freq=P_el_dc_per_bin_per_freq,
    #         eff_rep_bsm_detector_1=eff_rep_bsm_detector_1,
    #         eff_rep_bsm_detector_2=eff_rep_bsm_detector_2,
    #         P_rep_dc_per_bin_per_freq=P_rep_dc_per_bin_per_freq,
    #         eff_loading_qm=eff_loading_qm,
    #         eff_emitting_qm=eff_emitting_qm,
    #         mu=mu,
    #         num_elem_links=4
    #         )
    #     c_succ.append(rep_a.run()[1])
    #     c_fid.append(rep_a.run()[2])

    # plt.figure(figsize=(10, 5))
    # plt.plot(lengths, a_succ, label='1', color='blue')
    # plt.plot(lengths, b_succ, label='2', color='orange')
    # plt.plot(lengths, c_succ, label='3', color='green')
    # plt.xlabel('Distance (km)')

    # plt.ylabel('Success Rate (MHz)') 
    # plt.yscale('log')
    # plt.legend()
    # plt.grid()
    # plt.show()

    # plt.figure(figsize=(10, 5))
    # plt.plot(lengths, a_fid, label='1', color='blue')
    # plt.plot(lengths, b_fid, label='2', color='orange')
    # plt.plot(lengths, c_fid, label='3', color='green')
    # plt.xlabel('Distance (km)')     
    # plt.ylabel('Fidelity')
    # plt.legend()
    # plt.grid()
    # plt.show()


    ### SELECTING COMPONENTS IN TREE ###

    ### TESTING BTNS ###

    def print_network_button_clicked(self):
        print(self.network)

    def show_button_clicked(self):
        import networkx as nx
        import matplotlib.pyplot as plt

        print("Show Network button clicked")
        def draw_network(network):
            G = nx.DiGraph()

            # Add nodes
            for component in network.components:
                G.add_node(component.name)

            # Add edges based on links
            for link in network.links:
                G.add_edge(link.start.name, link.end.name)

            # Draw
            nx.draw(G, with_labels=True, node_color='lightblue', node_size=1500, arrowsize=20)
            plt.show()

        draw_network(self.network)
        