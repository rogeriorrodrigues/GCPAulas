from flask import json
from google.cloud import pubsub_v1

# Create a global Pub/Sub client to avoid unneeded network activity
pubsub = pubsub_v1.PublisherClient()


def recebeCompras(request):
    request_json = request.get_json(silent=True)
    json_data = request.args
    print('Monta JsonTemplate')
    json_template = {
        "Nome":None,
        'CPF':None,
        'Email':None,
        'Produto':None,
        'Quantidade':None,
        'Valor':None
    }
    # get json from request
    print('Inicio do Loop')
    # map data to json_template, we discard events not defined in template
    for key in json_data:
        try:
            if json_template[key] == None:
                if "timezone" in key and json_data[key] != None:
                    json_template[key] = json_data[key].split(".")[0]
                else:
                    json_template[key] = json_data[key]
                print("Valor - {}",format(json_data[key]))
        except KeyError:
            print('Value ' + key + ' not in template')
            pass
    
    print('Final do Loop e ennvio para PubSub')
    print(json_template)
    # publish json to Pub/Sub
    topic_name = 'projects/telefonica-digitalsales/topics/recebeVendas'
    pubsub.publish(topic_name, json.dumps(json_template).encode('utf-8'))
    print('Enviado para o PubSub')