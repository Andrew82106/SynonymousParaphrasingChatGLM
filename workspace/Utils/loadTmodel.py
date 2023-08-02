from transformers import AutoConfig, AutoModel, AutoTokenizer
import torch
import os
"""
# 载入Tokenizer
tokenizer = AutoTokenizer.from_pretrained("../../THUDM/chatglm2-6b", trust_remote_code=True)
config = AutoConfig.from_pretrained("../../THUDM/chatglm2-6b", trust_remote_code=True, pre_seq_len=128)
model = AutoModel.from_pretrained("../../THUDM/chatglm2-6b", config=config, trust_remote_code=True).cuda()
prefix_state_dict = torch.load(os.path.join("../../ptuning/output/adgen-chatglm2-6b-pt-128-2e-2/checkpoint-3000", "pytorch_model.bin"))
new_prefix_state_dict = {}
for k, v in prefix_state_dict.items():
    if k.startswith("transformer.prefix_encoder."):
        new_prefix_state_dict[k[len("transformer.prefix_encoder."):]] = v
model.transformer.prefix_encoder.load_state_dict(new_prefix_state_dict)
response, history = model.chat(tokenizer, "我今天下午在寝室里面吃了个包子", history=[])
print(response)
"""


class chatglm_ptuing:
    def __init__(self):
        self.route = "../THUDM/chatglm2-6b"
        self.ptuingRoute = "../ptuning/output/adgen-chatglm2-6b-pt-128-2e-2/checkpoint-3000"
        self.tokenizer = AutoTokenizer.from_pretrained(self.route, trust_remote_code=True)
        self.config = AutoConfig.from_pretrained(self.route, trust_remote_code=True, pre_seq_len=128)
        self.model = AutoModel.from_pretrained(self.route, config=self.config, trust_remote_code=True).cuda()
        self.prefix_state_dict = torch.load(os.path.join(self.ptuingRoute, "pytorch_model.bin"))
        self.new_prefix_state_dict = {}
        for k, v in self.prefix_state_dict.items():
            if k.startswith("transformer.prefix_encoder."):
                self.new_prefix_state_dict[k[len("transformer.prefix_encoder."):]] = v
        self.model.transformer.prefix_encoder.load_state_dict(self.new_prefix_state_dict)

    def response(self, textIn, history=None):
        try:
            if history is None:
                history = []
            res, history = self.model.chat(self.tokenizer, textIn, history=history)
            return res, history
        except Exception as e:
            return -1, e
