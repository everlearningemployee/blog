---
title: "Kafka를 공부해보자"
description: "Kafka 정도는 알아줘야지"
toc: true
layout: post
image: https://svn.apache.org/repos/asf/kafka/site/logos/originals/png/WIDE%20-%20Black%20on%20Transparent.png
categories: [kafka, hello]
---

![](Kafka.assets/download.png)

# PreStop Hook

구현 필요

# Consumer Group / Partition

- [Kafka 운영자가 말하는 Kafka Consumer Group](https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=1&ved=2ahUKEwis4s_no6zlAhUKvZQKHXC1ClQQFjAAegQIARAB&url=http%3A%2F%2Fwww.popit.kr%2Fkafka-consumer-group%2F&usg=AOvVaw2eqTWdayB-QZk7ez_CRru-)
  
  - 컨슈머 그룹 별로 각각 offset이 유지됨
  
  - 한 번 늘린 Partition은 줄일 수 없음
  
  - Partition갯수 > Consumer갯수:
    
    - 어쨌든 모두 다 일 함. 특정  Consumer로 일이 더 많이 쏠림
  
  - Partition갯수 < Consumer갯수
    
    - 노는 Consumr 생김. (우리는 이런 상황 절대 허용할 수 없음)

# ML(현 투입과제) 적용 전략

- K8s에 ML Logic Consumer Pod가 배포됐다고 치자

- Consumer Group은 **업무별로 1개**
  
  - 중복 처리 X이므로 여러 Consumer들이 Offset을 공유해야함

- Partition갯수와 Consumer갯수 매핑
  
  - partition은 consumming 과정이 동기인 듯 
    
    - 추정의 이유: 
      - 1개의 consumer는 1개 이상의 partition에 붙을 수 있으나
    - 1개의 partition은 1개의 consumer만 담당
    - 무조건 **Partition갯수 >= Consumer갯수**로 구성 필요
    - ML컨수머는 **롱트랜잭션**이므로
  
  - **1안) Partition갯수 = Consumer갯수: 1대 1로 갯수를 맞춤**
    
    - Consumer Pod를 **Scaling 하지 않음** (Min == Max)
      - 장점: 확실
    - 단점: Pod 리소스 점유 아까워
  
  - 2안) Partition갯수 = Max(Consumer갯수)
    
    - Consumer Pod를 Scaling 함
      - 장점: Pod 갯수 필요한 만큼 까지만 떠 있음
    - 단점: 업무 특성 상, Scale Out 시 모델 리스토어를 위하여 Pod ready 시간이 수십초~수분 소요 예상 ← 적절한 선택이 아님
  
  - 3안) Parition과 Cousumer 갯수는 테스트로 적정치 선정
    
    - Parition과 Cousumer의 **갯수 매핑** 자체는 실질적으로 의미가 **없음**
    
    - **전제**: Partition에 대한 메시지 배분이 라운드로빈이 아니라, **대기열이 가장 짧은 partition 우선**  
        ← Custom Partitioner  구현 필요?      
        ← 이미 준비되어있는 선택할 수 있는 Partitioner 유형이 있을 듯
      
      - Producer 생성 시, partitionerType 설정
        
        - default = 0, random = 1, cyclic = 2, keyed = 3, custom = 4
      
      - https://github.com/SOHU-Co/kafka-node/issues/1094
      
      - Parition과 Cousumer 각각의 **갯수 자체**가 의미 있음
      
      - 구찮... 3)안은 못 쓰겠다.

# 이슈

## Partitioner Type

- Producer 설정임
  - property: partitioner.class (default: kafka.producer.DefaultPartitioner)
- [Why is data not evenly distributed among partitions when a partitioning key is not specified?](https://cwiki.apache.org/confluence/display/KAFKA/FAQ#FAQ-Whyisdatanotevenlydistributedamongpartitionswhenapartitioningkeyisnotspecified?)

## Partition Rebalancing

- [Rebalancing Kafka partitions - TabMo Labs](https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=3&ved=2ahUKEwjxzp3J8qzlAhXDzIsBHcXjA0EQFjACegQIFhAB&url=https%3A%2F%2Flabs.tabmo.io%2Frebalancing-kafkas-partitions-803918d8d244&usg=AOvVaw0WNTNpYX_TAxnYxTLxSm2c)
- [Incremental Cooperative Rebalancing in Apache Kafka: Why Stop the World When You Can Change It?](https://www.confluent.io/blog/incremental-cooperative-rebalancing-in-kafka/)

## Rebalancing 지연

- [카프카 컨슈머 애플리케이션 배포 전략 - 11번가 사례](https://medium.com/11st-pe-techblog/%EC%B9%B4%ED%94%84%EC%B9%B4-%EC%BB%A8%EC%8A%88%EB%A8%B8-%EC%95%A0%ED%94%8C%EB%A6%AC%EC%BC%80%EC%9D%B4%EC%85%98-%EB%B0%B0%ED%8F%AC-%EC%A0%84%EB%9E%B5-4cb2c7550a72)
- 그룹 내 특정 컨슈머가 poll 메소드를 호출을 지연
- 모든 컨슈머가 poll  해야 rebalancing 진행

## NiFi 연동

- [PublishKafka](https://nifi.apache.org/docs/nifi-docs/components/org.apache.nifi/nifi-kafka-0-9-nar/1.5.0/org.apache.nifi.processors.kafka.pubsub.PublishKafka/)
  - Partitioner class에 아래 2개 밖에 없음
    - RoundRobinPartitioner 
      Messages will be assigned partitions in a round-robin fashion, sending the first message to Partition 1, the next Partition to Partition 2, and so on, wrapping as necessary.
    - DefaultPartitioner 

# Consumer Option

- [Kafka - Kafka Consumer(카프카 컨슈머) Java&CLI - 코딩스타트](https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=2&ved=2ahUKEwis4s_no6zlAhUKvZQKHXC1ClQQFjABegQIAhAB&url=https%3A%2F%2Fcoding-start.tistory.com%2F137&usg=AOvVaw0ygVeIKyALE-u0C4ernoJG)

| Option                   | 내용                                                                                                                                                                                                            | 컨수머 설정                    |
| ------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------- |
| **bootstrap.servers**    | 호스트와 포트 정보로 구성된 리스트                                                                                                                                                                                           |                           |
| **group.id**             | 컨슈머 그룹 식별자                                                                                                                                                                                                    | 업무별 1개                    |
| **auto.offset.reset**    | 오프셋이 없거나 현재 오프셋이 더 이상 존재하지 않은 경우 (**earliest**가장초기/**latest**마지막/**none**에러)                                                                                                                                  | latest                    |
| **fetch.min.bytes**      | 한번에 가져올 수 있는 최소 데이터 사이즈이다. 만약 지정한 사이즈보다 작은 경우, 요청에 대해 응답하지 않고 데이터가 누적될 때까지 기다린다                                                                                                                               | 뭐지? 확인 필요. 작아야하나?         |
| **fetch.max.bytes**      | 한번에 가져올 수 있는 최대 데이터 사이즈                                                                                                                                                                                       | 확인 필요. 별로 안 커도 될듯         |
| **request.timeout.ms**   | 요청에 대해 응답을 기다리는 최대 시간                                                                                                                                                                                         | 뭐지? 확인 필요. 별로 안 커도 될듯     |
| **session.timeout.ms**   | 컨슈머와 브로커사이의 세션 타임 아웃시간. 브로커가 컨슈머가 살아있는 것으로 판단하는 시간(기본값 10초)                                                                                                                                                   | **롱트랜잭션이므로 충분히 길게**       |
| **hearbeat.interval.ms** | 그룹 코디네이터에게 얼마나 자주  KafkaConsumer poll() 메소드로 하트비트를 보낼 것인지 조정한다. session.timeout.ms와 밀접한 관계가  있으며 session.timeout.ms보다 낮아야한다. 일반적으로 1/3 값정도로 설정한다.(기본값 3초)                                                     | 이거이거 확인 필요. **우리는 롱트랜잭션** |
| **max.poll.records**     | 단일 호출 poll()에 대한 최대 레코드 수를 조정한다. 이 옵션을 통해 애플리케이션이 폴링 루프에서 데이터를 얼마나 가져올지 양을 조정할 수 있다                                                                                                                           | 뭐지?                       |
| **max.poll.interval.ms** | 컨슈머가 살아있는지를 체크하기 위해  하트비트를 주기적으로 보내는데, 컨슈머가 계속해서 하트비트만 보내고 실제로 메시지를 가져가지 않는 경우가 있을 수도 있다. 이러한  경우 컨슈머가 무한정 해당 파티션을 점유할 수 없도록 주기적으로 poll을 호출하지 않으면 장애라고 판단하고 컨슈머 그룹에서  제외한 후 다른 컨슈머가 해당 파티션에서 메시지를 가져갈 수 있게한다. | 이거이거 확인 필요. **우리는 롱트랜잭션** |

```
# Kafka 토픽
topic: diff-ai
# 업무단위: 정책 상 토픽과 1:1
group_id: mymyGrp
# Kafka 서버
bootstrap_servers: localhost:9092
# 오프셋이 없거나 현재 오프셋이 더 이상 존재하지 않은 경우 
# earliest:가장초기, latest마지막, none:에러
auto_offset_reset: latest
# 컨슈머와 브로커사이의 세션 타임 아웃시간 (초). 브로커가 컨슈머가 살아있는 것으로 판단하는 시간
# ML컨수머는 롱트랜잭션이므로 충분히 길게 설정할 것
session_timeout_ms: 1200
# 롱트랜잭션이며 새로 추가되는 pod가 메시지를 즉시 받아올 수 있도록 1로 설정
max_poll_records: 1
```

# Hello Kafka

### Topic 만들기

```bash
kafka-topics.bat --create --zookeeper localhost:2181 --replication-factor 1 --partitions 4 --topic diff-ai

kafka-topics.bat --zookeeper localhost:2181 --list
```

### Producer 콘솔 기동

```bash
kafka-console-producer --broker-list localhost:9092 --topic diff-ai
kafka-console-producer --broker-list localhost:9092 --topic mymy-A < ..\..\..\Test\TestData\short_input.txt
```

### Consumer 콘솔 기동

```bash
kafka-console-consumer --bootstrap-server localhost:9092 --topic diff-ai --group mymyGrp
kafka-console-consumer --bootstrap-server loclahost:9092 --topic mymy-B --group mymyGrp
```

### Topic alter

```bash
kafka-topics --alter --zookeeper localhost:2181 --topic diff-ai --partitions 4
```

- Kafka port: 9092

- Zookeeper port: 2181

- [Hello world in Kafka using Python - Timber.io](https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=2&ved=2ahUKEwjWpPjcsLHlAhWMJaYKHUffDi8QFjABegQIBBAB&url=https%3A%2F%2Ftimber.io%2Fblog%2Fhello-world-in-kafka-using-python%2F&usg=AOvVaw3zKbjel1WRwgyoEhDahl1g)

# Python Lib

- [구글 트랜드 결과](https://trends.google.co.kr/trends/explore?q=%22kafka-python%22,PyKafka,%22confluent-kafka%22)
  [kafka-python](https://github.com/dpkp/kafka-python) > [PyKafka](https://github.com/Parsely/pykafka) > [confluent-kafka-python](https://github.com/confluentinc/confluent-kafka-python)

- 처리속도 비교 

- [Kafka Python client 성능 테스트](https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=2&ved=2ahUKEwjckIqvvrHlAhWIQN4KHYQ0AqwQFjABegQIARAB&url=http%3A%2F%2Fwww.popit.kr%2Fkafka-python-client-%EC%84%B1%EB%8A%A5-%ED%85%8C%EC%8A%A4%ED%8A%B8%2F&usg=AOvVaw3Q4mrA8RW8xRXFcBd2tmD5) (원본자료: [Python Kafka Client Benchmarking 2016-06-15](http://activisiongamescience.github.io/2016/06/15/Kafka-Client-Benchmarking/#Python-Kafka-Client-Benchmarking)) 

- https://kafka-python.readthedocs.io/en/master/apidoc/modules.html

- [kafka-python](https://github.com/dpkp/kafka-python) 헬로우월드
  
  - Consumer
    
    ```python
    from kafka import KafkaConsumer
    import time
    
    consumer = KafkaConsumer('diff-ai', 
                             group_id='mymyGrp', 
                             bootstrap_servers='localhost:9092')
    
    for message in consumer:
        print("\n"+"="*60)
        print(message.value)
        print("-"*60)
        #time.sleep(1)
    
    consumer.close()
    ```

# 모니터링

- [Apache kafka 모니터링을 위한 Metrics 이해 및 최적화 방안](https://www.slideshare.net/freepsw/apache-kafka-metrics-123663954)
- Burrow
  - https://github.com/linkedin/Burrow
  - [Kafka Consumer Lag 모니터링, Burrow를 알아보자 (1)](https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=2&ved=2ahUKEwiyl93D8rHlAhWQbN4KHW81B_AQFjABegQIAhAB&url=https%3A%2F%2Fdol9.tistory.com%2F272&usg=AOvVaw38_uV7jfhMRQjHFyAPXSuZ)
  - [Monitoring Kafka with Burrow - Part 1 - Cloudera Community](https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=1&ved=2ahUKEwjZidSW-LHlAhXdzIsBHXsEDagQFjAAegQIABAB&url=https%3A%2F%2Fcommunity.cloudera.com%2Ft5%2FCommunity-Articles%2FMonitoring-Kafka-with-Burrow-Part-1%2Fta-p%2F245987&usg=AOvVaw2mXcK_5vPKZqamVCHFyw72)
- [Apache ZooKeeper 소개 - SlideShare](https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=9&ved=2ahUKEwjenIqN87HlAhVDE4gKHb6WCBkQFjAIegQINBAB&url=https%3A%2F%2Fwww.slideshare.net%2Fsunnykwak90%2Fapache-zoo-keeper&usg=AOvVaw0PpQfiNhFgyy1PqB9LdBpq)
