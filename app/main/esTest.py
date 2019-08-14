#测试elasticsearch能否使用，今后项目优化的时候可以做
from elasticsearch import Elasticsearch

#连接到es服务器地址，设置超时时间
es = Elasticsearch(['10.10.21.178'],timeout=360)

data = {
    'mappings':{
        'properties':{
            'title':{
                'type':'text',
                'index':True
            },
            'keywords': {
                'type': 'string',
                'index': True
            },
            'content': {
                'type': 'text',
                'index': True
            },

        }
    }
}


es.indices.create(index='pythonTest',body=data)