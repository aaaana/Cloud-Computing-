from kafka import KafkaConsumer

consumer=KafkaConsumer('input_recommend_product',
bootstrap_servers=['localhost:9092'])
for msg in consumer:
    print(msg)
