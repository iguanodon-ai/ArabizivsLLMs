<a href="https://iguanodon.ai"><img src="img/iguanodon.ai.png" width="125" height="125" align="right" /></a>

# ArabizivsLLMs

This is the code for the paper "Arabizi vs LLMs: Can the Genie Understand the Language of Aladdin?" (Al Almaoui, Bouillon, Hengchen), to be published at MT Summit 2025. 

**Paper abstract**:
> In this era of rapid technological advancements, communication continues to evolve as new linguistic phenomena emerge. Among these is Arabizi, a hybrid form of Arabic that incorporates Latin characters and numbers to represent the spoken dialects of Arab communities. Arabizi is widely used on social media and allows people to communicate in an informal and dynamic way, but it poses significant challenges for machine translation due to its lack of formal structure and deeply embedded cultural nuances. This case study arises from a growing need to translate Arabizi for gisting purposes. It evaluates the capacity of different LLMs to decode and translate Arabizi, focusing on multiple Arabic dialects that have rarely been studied up until now. Using a combination of human evaluators and automatic metrics, this research project investigates the models’ performance in translating Arabizi into both Modern Standard Arabic and English. Key questions explored include which dialects are translated most effectively and whether translations into English surpass those into Arabic.

**URL**: https://arxiv.org/abs/2502.20973

**Dataset**: https://huggingface.co/datasets/palmaoui/AladdinBench

**Bibtex**: 
```
@article{almaoui2025arabizi,
  title={Arabizi vs LLMs: Can the Genie Understand the Language of Aladdin?},
  author={Al Almaoui, Perla and Bouillon, Pierrette and Hengchen, Simon},
  journal={arXiv preprint arXiv:2502.20973},
  year={2025}
}
```

## Getting Started

### Setting up the Environment

1. Create a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate   # On Windows: venv\Scripts\activate
    ```

2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Launch a local litellm proxy instance and/or adapt the code in `utils.py` to wherever you host/access LLMs (see: https://github.com/BerriAI/litellm)

4. Create a `.env` file with your secrets

5. See `launch.sh` for examples on how to run the code

## Notes

1. This code was written when the dataset was still a bunch of excel files. If you use the Huggingface version (https://huggingface.co/datasets/palmaoui/AladdinBench) a lot of this code is superfluous


2. Get in touch by email or open an issue if you encounter any issue


## License and contact

This code is made available to the public <a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/">under the permissive CC BY-NC-SA 4.0 license</a>.

 <a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png" /></a>
