**Paper**: Low-rank Angular Prior Guided Multi-diffusion Model for Few-shot Low-dose CT Reconstruction         
IEEE Transactions on Computational Imaging, Vol. 10, pp. 1763-1774, 2024.     
**Authors**: Wenhao Zhang, Bin Huang, Shuyue Chen, Xiaoling Xu, Weiwen Wu, Qiegen Liu      
https://ieeexplore.ieee.org/abstract/document/10776993     
     
The code and the algorithm are for non-comercial use only. Copyright 2024, School of Information Engineering, Nanchang University.

Low-dose computed tomography (LDCT) is essential in clinical settings to minimize radiation exposure; however, reducing the dose often leads to a significant decline in image quality. Additionally, conventional deep learning approaches typically require large datasets, raising con-cerns about privacy, costs, and time constraints. To ad-dress these challenges, a few-shot low-dose CT reconstruc-tion method is proposed, utilizing low-Rank Angular Pri-or (RAP) multi-diffusion model. In the prior learning phase, projection data is transformed into multiple con-secutive views organized by angular segmentation, allow-ing for the extraction of rich prior information through low-rank processing. This structured approach enhances the learning capacity of the multi-diffusion model. Dur-ing the iterative reconstruction phase, a stochastic differ-ential equation solver is employed alongside data con-sistency constraints to iteratively refine the acquired pro-jection data. Furthermore, penalized weighted least-squares and total variation techniques are integrated to improve image quality. Results demonstrate that the re-constructed images closely resemble those obtained from normal-dose CT, validating the RAP model as an effec-tive and practical solution for artifact and noise reduc-tion while preserving image fidelity in low-dose situation.

## The training pipeline of RAP
![](img/fig1.png)

## The pipeline for iterative reconstruction stage of RAP
![](img/fig2.png)

## Reconstruction results from 1e4 noise level using different methods
![](img/fig3.png)
(a) The reference image, (b) FBP, (c) SART-TV, (d) CNN, (e) NCSN++, (f) U-ViT, (g) OSDM, (h) RAP (1).

## Train
```
python main_up.py --config=aapm_sin_ncsnpp_up.py --workdir=exp1_up --mode=train --eval_folder=result1_up
python main_middle.py --config=aapm_sin_ncsnpp_middle.py --workdir=exp1_middle --mode=train --eval_folder=result1_middle
python main_down.py --config=aapm_sin_ncsnpp_down.py --workdir=exp1_down  --mode=train --eval_folder=result1_down
```


## Test
```
python PCsampling_demo.py
```

### Other Related Projects
<div align="center"><img src="https://github.com/yqx7150/OSDM/blob/main/All-CT.png" >  </div>   
    
  * Generative Modeling in Sinogram Domain for Sparse-view CT Reconstruction      
[<font size=5>**[Paper]**</font>](https://ieeexplore.ieee.org/document/10233041)   [<font size=5>**[Code]**</font>](https://github.com/yqx7150/GMSD)

  * One Sample Diffusion Model in Projection Domain for Low-Dose CT Imaging  
[<font size=5>**[Paper]**</font>](https://ieeexplore.ieee.org/abstract/document/10506793)   [<font size=5>**[Code]**</font>](https://github.com/yqx7150/OSDM)

  * Iterative Reconstruction for Low-Dose CT using Deep Gradient Priors of Generative Model  
[<font size=5>**[Paper]**</font>](https://ieeexplore.ieee.org/abstract/document/9703672)   [<font size=5>**[Code]**</font>](https://github.com/yqx7150/EASEL)   [<font size=5>**[PPT]**</font>](https://github.com/yqx7150/HGGDP/tree/master/Slide)
    
  * REDAEP: Robust and Enhanced Denoising Autoencoding Prior for Sparse-View CT Reconstruction  
[<font size=5>**[Paper]**</font>](https://ieeexplore.ieee.org/document/9076295)   [<font size=5>**[Code]**</font>](https://github.com/yqx7150/REDAEP)   [<font size=5>**[PPT]**</font>](https://github.com/yqx7150/HGGDP/tree/master/Slide)

  * Wavelet-improved score-based generative model for medical imaging  
[<font size=5>**[Paper]**</font>](https://ieeexplore.ieee.org/abstract/document/10288274)

  * 基于深度能量模型的低剂量CT重建  
[<font size=5>**[Paper]**</font>](http://cttacn.org.cn/cn/article/doi/10.15953/j.ctta.2021.077)   [<font size=5>**[Code]**</font>](https://github.com/yqx7150/EBM-LDCT)  

 * Stage-by-stage Wavelet Optimization Refinement Diffusion Model for Sparse-view CT Reconstruction  
[<font size=5>**[Paper]**</font>](https://ieeexplore.ieee.org/abstract/document/10403850)   [<font size=5>**[Code]**</font>](https://github.com/yqx7150/SWORD)

  * Dual-Domain Collaborative Diffusion Sampling for Multi-Source Stationary Computed Tomography Reconstruction  
[<font size=5>**[Paper]**</font>](https://ieeexplore.ieee.org/document/10577271)   [<font size=5>**[Code]**</font>](https://github.com/lizrzr/DCDS-Dual-domain_Collaborative_Diffusion_Sampling)
  
  * Physics-informed DeepCT: Sinogram Wavelet Decomposition Meets Masked Diffusion  
[<font size=5>**[Paper]**</font>](https://arxiv.org/abs/2501.09935)   [<font size=5>**[Code]**</font>](https://github.com/yqx7150/SWARM)    
                    
  * MSDiff: Multi-Scale Diffusion Model for Ultra-Sparse View CT Reconstruction  
[<font size=5>**[Paper]**</font>](https://arxiv.org/pdf/2405.05763)   [<font size=5>**[Code]**</font>](https://github.com/yqx7150/MSDiff)

  * Ordered-subsets Multi-diffusion Model for Sparse-view CT Reconstruction      
[<font size=5>**[Paper]**</font>](https://arxiv.org/abs/2505.09985)
                          
  * Virtual-mask Informed Prior for Sparse-view Dual-Energy CT Reconstruction  
[<font size=5>**[Paper]**</font>](https://arxiv.org/abs/2504.07753)   [<font size=5>**[Code]**</font>](https://github.com/yqx7150/VIP-DECT)

  * Raw_data_generation  [<font size=5>**[Code]**</font>](https://github.com/yqx7150/Raw_data_generation)

  * PRO: Projection Domain Synthesis for CT Imaging  [<font size=5>**[Paper]**</font>](https://arxiv.org/pdf/2506.13443)   [<font size=5>**[Code]**</font>](https://github.com/yqx7150/PRO)
       
  * UniSino: Physics-Driven Foundational Model for Universal CT Sinogram Standardization[<font size=5>**[Paper]**</font>](https://arxiv.org/abs/2508.17816)   [<font size=5>**[Code]**</font>](https://github.com/yqx7150/UniSino)

  * Diffusion Models for Medical Imaging
[<font size=5>**[Paper]**</font>](https://github.com/yqx7150/Diffusion-Models-for-Medical-Imaging)   [<font size=5>**[Code]**</font>](https://github.com/yqx7150/Diffusion-Models-for-Medical-Imaging)   [<font size=5>**[PPT]**</font>](https://github.com/yqx7150/HKGM/tree/main/PPT) 





