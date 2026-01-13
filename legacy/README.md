# Replication Package: Performance Modeling and Analysis of Design Patterns for Microservice Systems

[![DOI](https://zenodo.org/badge/560469456.svg)](https://zenodo.org/badge/latestdoi/560469456)  
This package contains performance models and results of seven cloud design patterns analyzed in the paper *"Performance Modeling and Analysis of Design Patterns for Microservice Systems"* accepted for publication in the 20th IEEE International Conference on Software Architecture (ICSA 2023).


## Authors
Riccardo Pinciroli (Gran Sasso Science Institute), Italy  
Aldeida Aleti (Monash University), Australia  
Catia Trubiani (Gran Sasso Science Institute), Italy


## Abstract
*Context.* The adoption of design patterns in the microservice architecture and cloud-native development scope was recently reviewed to investigate the industry practice. Interestingly, when considering performance-related aspects, practitioners focus on specific metrics (e.g., the time taken to handle requests) to identify sources of performance hindrance.

*Objective.* This paper investigates a subset of seven design patterns that industrial practitioners indicate as relevant for system performance. We are interested to quantify the impact of these patterns while considering heterogeneous workloads, thus supporting software architects in understanding the root causes of performance issues. 

*Method.* We use queuing networks to build the performance models of the seven design patterns and extract quantitative insights from model-based performance analysis. Our performance models are flexible in their input parameterization and reusable in different application contexts. 

*Results.* We find that most design patterns confirm the expectation of practitioners, and our experimental results assess the identified performance gains and pains. One design pattern (i.e., Gateway Offloading) shows the peculiar characteristic of contributing to performance pains in some cases, leading to novel insights about the impact of design patterns in microservice systems.


## Available Files
- <tt>sim\_time\_analysis.ipynb</tt> that provides statistics and distributions of the simulation time.
- <tt>varEnv.py</tt> where the location of the simulator (JAR file) and the number of concurrent simulations to run is specified.
- <tt>Images/</tt> that contains figures (and some source files) presented in the paper.
- A folder for each one of the seven cloud design patterns analyzed in the paper.
- All these folders (except <tt>CQRS/</tt> and <tt>Pipes\_and\_Filters/</tt>) are organized as follows:
  - <tt>analysis.ipynb</tt> is a Juoyter notebook that allows plotting the figures in the paper
  - <tt>model.placeholder.jsimg</tt> is the JMT model used for simulations. Users should not change this file unless they want to model new design patterns or update old models.
  - <tt>runSim.py</tt> is the Python script that run the simulations. Users can tune input parameters contained in this file to analyze their own applications.
  - At least one <tt>CSV</tt> file containing the simulation results used in the paper.
- In <tt>CQRS/</tt> there are two sub-folders (<tt>separated\_HW/</tt> and <tt>separated\_SW/</tt>) for simulating the two implementations of this design pattern and a single <tt>analysis.ipynb</tt> file for analyzing the results.
- In <tt>Pipes\_and\_Filters/</tt> there are two sub-folders (<tt>joint/</tt> and <tt>separated/</tt>) for simulating the two implementations of this design pattern and a single <tt>analysis.ipynb</tt> file for analyzing the results.


## Prerequisites
- Python 3.8.10
- Users can install required Python modules by running <tt>pip3 install -r requirements.txt</tt>
- Java Modelling Tools (JMT), download the [JAR version](http://sourceforge.net/projects/jmt/files/jmt/JMT-1.2.2/JMT-singlejar-1.2.2.jar/download). After downloading the JAR file, change the *jmtpath* variable in <tt>varEnv.py</tt> with the path of the newly downloaded file.
  - [Oracle/Sun Java Runtime Environment](http://www.oracle.com/technetwork/java/javase/downloads/index.html) (version 1.6 or later) or [OpenJDK](https://openjdk.org/install/) (version 9 or later)


## Run a simulation
To run a simulation, please check the README file in the folder of the desired design pattern.
- [Anti-corruption Layer](Anti\_Corruption\_Layer/)
- [Backends for Frontends](Backends\_for\_Frontends/)
- [CQRS](CQRS/)
- [Gateway Aggregation](Gateway\_Aggregation/)
- [Gateway Offloading](Gateway\_Offloading/)
- [Pipes and Filters](Pipes\_and\_Filters/)
- [Static Content Hosting](Static\_Content\_Hosting/)
