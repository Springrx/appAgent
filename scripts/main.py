import os
from volcengine.maas import MaasService, MaasException, ChatRole

def test_chat(maas, req):
    try:
        resp = maas.chat(req)
        print(resp)
        print(resp.choice.message.content)
    except MaasException as e:
        print(e)
def construct_req(prompt):
    req = {
        "model": {
            "name": "skylark2-pro-4k",  # 这里根据模型不同，设置不同的model_name
            "version": "1.1",  # 设置调用模型的版本号
        },
        "parameters": {
            "max_new_tokens": 1000,  # 输出文本的最大tokens限制
            "min_new_tokens": 1,  # 输出文本的最小tokens限制
            "temperature": 0.01,  # 用于控制生成文本的随机性和创造性，Temperature值越大随机性越大，取值范围0~1
            "top_p": 0.7,  # 用于控制输出tokens的多样性，TopP值越大输出的tokens类型越丰富，取值范围0~1
            "top_k": 0,  # 选择预测值最大的k个token进行采样，取值范围0-1000，0表示不生效
            "max_prompt_tokens": 3000,  # 最大输入 token 数，如果给出的 prompt 的 token 长度超过此限制，取最后 max_prompt_tokens 个 token 输入模型。
            "repetition_penalty": 1.1  # 重复token输出的惩罚项
        },
        # 如果是单轮对话，构造message的方式
        "messages": [
            {
                "role": ChatRole.USER,
                "content": prompt
            }
        ]
        # # 如果是多轮对话，构造message的方式
        # "messages": [
        #     {
        #         "role": ChatRole.USER,
        #         "content": "我对北京的美食很感兴趣，你能给我一些推荐吗？"
        #     }, {
        #         "role": ChatRole.ASSISTANT,
        #         "content": "没问题，北京有很多著名的美食，比如烤鸭、老北京炸酱面、涮羊肉等。你有特别喜欢的口味或者菜系吗？"
        #     }, {
        #         "role": ChatRole.USER,
        #         "content": "我比较喜欢川菜，有没有川菜馆推荐呢？"
        #     }
        # ]
    }
    return req
if __name__ == '__main__':
    # 如果调用的时候，遇到Read time out问题，可以尝试调大connection_timeout和socket_timeout
    maas = MaasService('maas-api.ml-platform-cn-beijing.volces.com', 'cn-beijing', connection_timeout=600, socket_timeout=600)

    # 设置客户或者个人在方舟账号的ak，sk
    maas.set_ak(os.getenv("AKLTYmU2YzMwZWY3NDkwNGZiMDg2ODExYTc2MGVjZjYxNzg"))
    maas.set_sk(os.getenv("WldNNE1qZ3laR1ZqWldOa05ESTNNemhtTldWaU56TXpOR0ZrWkdNME5XWQ=="))

    prompt = '''
    为一群10-15岁的孩子编写一篇介绍太空探索历史的文章。
    '''

    # chat接口调用
    test_chat(maas, construct_req(prompt))
