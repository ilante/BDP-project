# Building a Small Computing Infrastructure as a Service in the Cloud

1. Install & configuer as Batch System &rarr; HTCondor
  * 1 Master Node
  * At least 2 WN
* Creating shared volume accessible to ALL nodes

2. Scientific application chosen: [libsvm](https://www.csie.ntu.edu.tw/~cjlin/libsvm/) svm-train
  * Idea: training 2 SVM models for protein secondary structure (SS) prediction using Radial Basis Funciton (RBF) kernel
    * Motivation: grid-searches are useful for finding the right hyperparameters *C* (Cost) and $\gammma$
    * For the scope of the project only 2 models will be trained
       * Can be scaled up easily for a larger grid-search to find best hyperparameters
       
  * Create test jobs
  * Input and output must be handled by **Sandbox** or **Shared Volume**
  * Discuss model for data management that was chosen for the application
  * Justify choices
  * Describe SVM and the structure of the jobs
  * Run the test jobs
3. Create container image that can be used to run:
  * Application
  * Test jobs
4. Evaluate the **time needed** to address several runs
  * Discuss dimension needed
  * Estimate costs
