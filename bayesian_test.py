import pysmile

pysmile.License((
    b"SMILE LICENSE b9920ff8 e8376d62 e10f1514 "
    b"THIS IS AN ACADEMIC LICENSE AND CAN BE USED "
    b"SOLELY FOR ACADEMIC RESEARCH AND TEACHING, "
    b"AS DEFINED IN THE BAYESFUSION ACADEMIC "
    b"SOFTWARE LICENSING AGREEMENT. "
    b"Serial #: 3b87myllo578uo83naj9qmgi "
    b"Issued for: dung nguyen (nguyendung30021109@gmail.com) "
    b"Academic institution: abc123 "
    b"Valid until: 2025-03-31 "
    b"Issued by BayesFusion activation server"
),[
    0xc8,0xe2,0x47,0x04,0xd2,0x44,0xec,0xde,0x2b,0x40,0xd8,0xd7,0xdb,0xf4,0xc4,0xb4,
    0xb2,0x88,0x07,0x97,0xce,0x90,0x84,0x89,0x24,0x63,0xa4,0x97,0x23,0x7c,0xf5,0x30,
    0x4e,0x83,0xfc,0x98,0xc5,0xe8,0x28,0x46,0xc4,0x3f,0x0e,0x74,0x3c,0x26,0xfb,0x04,
    0xb3,0x43,0x51,0xc8,0xbc,0x4d,0x46,0x4a,0x97,0xed,0xfa,0xe1,0x56,0xa0,0x6d,0x34])

class AttackerDefenderDBN:
    def __init__(self, supplement_config):
        print("Setting up Attacker-Defender DBN...")
        self.net = pysmile.Network()
        
        self.attacker_nodes = []
        attacker_score = []

        for capability in supplement_config["attacker_capability"]:
            node = self.create_cpt_node(
                self.net,
                capability["name"],
                capability["name"],
                ["0", "2"],
                100, 100 
            )
            self.attacker_nodes.append(node)
            attacker_score.append(capability["score"])
            self.net.set_node_temporal_type(node, pysmile.NodeTemporalType.PLATE)

        attacker_capability_cpt = self.create_cpt_node(
            self.net, 
            "attacker_capability_cpt", 
            "Attacker Capability CPT", 
            ["0", "1"],
            500, 100
        )

        self.net.set_node_temporal_type(attacker_capability_cpt, pysmile.NodeTemporalType.PLATE)

        for node in self.attacker_nodes:
            self.net.add_arc(node, attacker_capability_cpt)

        self.set_initial_cpt_attacker(attacker_capability_cpt, attacker_score)

        self.net.add_temporal_arc(attacker_capability_cpt, attacker_capability_cpt, 1)

        self.set_initial_temporal_cpt_attacker(attacker_capability_cpt, attacker_score)

        self.net.set_slice_count(5)
        print("Attacker-Defender DBN setup complete.")

    def create_cpt_node(self, net, id, name, outcomes, x_pos, y_pos):
        handle = net.add_node(pysmile.NodeType.CPT, id)
        net.set_node_name(handle, name)
        net.set_node_position(handle, x_pos, y_pos, 85, 55)
        
        # Thiết lập outcomes cho node
        initial_outcome_count = net.get_outcome_count(handle)
        for i in range(len(outcomes)):
            if i < initial_outcome_count:
                net.set_outcome_id(handle, i, outcomes[i])
            else:
                net.add_outcome(handle, outcomes[i])
        
        return handle

    def set_initial_cpt_attacker(self, attacker_node, attacker_score):

        attacker_cpt_values= [0.5, 0.1, 0.2, 0.3 , 0.4 , 0.6,  0.7,  0.8 ]
        self.net.set_node_definition(attacker_node, attacker_cpt_values)

    def set_initial_temporal_cpt_attacker(self, attacker_node, attacker_score):
        # attacker_def_temporal = [0.5 for _ in range(16)]
        attacker_def_temporal= [0.5, 0.1, 0.2, 0.3 , 0.4 , 0.6,  0.7,  0.8
                              ,  0.9, 0.3,  0.22,  0.11,  0.15,  0.6,  0.99,  0.12
                              ]
        self.net.set_node_temporal_definition(attacker_node, 1, attacker_def_temporal)

    def update_and_show_results(self):
        self.net.update_beliefs()
        slice_count = self.net.get_slice_count()

        for h in self.net.get_all_nodes():
            if self.net.get_node_temporal_type(h) == pysmile.NodeTemporalType.PLATE:
                outcome_count = self.net.get_outcome_count(h)
                values = self.net.get_node_value(h)
                print(f"Temporal beliefs for {self.net.get_node_id(h)}:")
                for slice_idx in range(slice_count):
                    print(f"\tt={slice_idx}:", end="")
                    for i in range(outcome_count):
                        print(f" {values[slice_idx * outcome_count + i]:.4f}", end=" ")
                    print()

def main():
    supplement_config = {
        "deployment_scenario_id": "65f5f79e690a4b0a94b599f2",
        "attacker_aggregate_function": "mean",
        "defender_aggregate_function": "mean",
        "attacker_variation_rate": 0.03,
        "defender_variation_rate": 0,
        "effectiveness_defender": [
            {"score": 5, "name": "Security_Awareness_Training", "type": "organizational", "weight": 1},
            {"score": 4, "name": "Security_Monitoring", "type": "technical", "weight": 1}
            # {"score": 6, "name": "Vulnerability_Management", "type": "technical", "weight": 1},
            # {"score": 6, "name": "Incident_Response_Plan", "type": "organizational", "weight": 1},
            # {"score": 5, "name": "Log_Management", "type": "technical", "weight": 1}
        ],
        "attacker_capability": [
            {"score": 8, "name": "Specialist_Expertise", "type": "mean", "weight": 1},
            {"score": 9, "name": "Knowledge_Of_The_System", "type": "mean", "weight": 1}
            # {"score": 6, "name": "Equipment_And_Tools", "type": "mean", "weight": 1},
            # {"score": 7, "name": "Elapsed_Time", "type": "opportunity", "weight": 1},
            # {"score": 5, "name": "Window_Of_Opportunity", "type": "opportunity", "weight": 1}
        ]
    }

    dbn = AttackerDefenderDBN(supplement_config)

    dbn.update_and_show_results()

if __name__ == "__main__":
    main()
