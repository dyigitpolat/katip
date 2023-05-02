from katip.content_generation.document_generator import DocumentGenerator

import json
import os

abstract = """This paper presents MimarSinan, an end-to-end hardware-aware spiking neural network architecture search (NAS) framework for neuromorphic AI accelerators. MimarSinan aims to optimize the performance and energy efficiency of spiking neural networks (SNNs) by jointly searching for the SNN topology, neuron model, and synaptic model. Unlike existing NAS frameworks, MimarSinan considers hardware-specific constraints and characteristics such as the number of available resources, the dataflow of the accelerator, and the energy consumption of the circuits. To efficiently explore the vast design space, MimarSinan employs a gradient-based optimization algorithm and a surrogate model to approximate the hardware cost of the searched architectures. Experimental results demonstrate that MimarSinan can find high-performance SNN architectures that outperform state-of-the-art designs while meeting the hardware constraints. MimarSinan is a promising approach to enable the design of efficient neuromorphic AI accelerators with improved accuracy and energy consumption."""

if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    os.makedirs("../generated", exist_ok=True)

    document_dict = DocumentGenerator().generate_from_abstract(abstract)

    json.dump(document_dict, open("../generated/document.json", "w"))