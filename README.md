## ECE515 Mobile-and-Pervasive-Computing
Project Title: Simulation of Cone-Based Topology Control (CBTC)

### Objective
This project implements the Cone-Based Topology Control (CBTC) algorithm, based on the research paper: \\\
*"A Cone-Based Distributed Topology-Control Algorithm for Wireless Multi-Hop Networks" by Li, Halpern, Bahl, Wang, and Wattenhofer (Microsoft Research, Cornell, ETH Zurich)*
The CBTC algorithm reduces transmission power and redundant links in wireless ad hoc networks while maintaining connectivity by ensuring each node has at least one neighbor in every cone of a given angular width.

### Project Goals
- Implement the CBTC algorithm in Python
- Simulate multi-hop wireless networks with 100 nodes
- Visualize different topology scenarios based on:
  - Cone angle (e.g., 2π/3, 5π/6)
  - Shrink-back optimization
  - Asymmetric edge removal
- Evaluate the effect of each configuration on connectivity and power efficiency

📁 Files
- cbtc_simulation.py: Main Python script that implements the CBTC algorithm and its optimizations
- MPC_Alexandra_Gianni_3382_report.pdf: Report with theoretical background, implementation details, and performance evaluation
- CBTC.pdf: Original academic paper that inspired the implementation
