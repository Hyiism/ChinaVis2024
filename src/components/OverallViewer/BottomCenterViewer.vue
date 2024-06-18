<template>
    <div>
      <button @click="sendMessage">发送消息</button>
      <button @click="sendMessage1">发送消息1</button>
      <button @click="sendMessage2">发送消息2</button>
      <button @click="sendMessage3">发送消息3</button>
      <div>
        最新消息: {{ latestMessage }}
      </div>
    </div>
  </template>
  
  <script>
  import PubSub from 'pubsub-js';
  
  export default {
    name: 'PubSubExample',
    data() {
      return {
        latestMessage: '',
        latestTimestamp: 0,
      };
    },
    methods: {
      sendMessage() {
        const message = { title_ID: '4nHcauCQ0Y6Pm8DgKlLo', timestamp: Date.now() };
        PubSub.publish('title_ID', message);
        console.log(`消息已发送: ${message.title_ID} at ${message.timestamp}`);
      },
      sendMessage1() {
        const message = { title_ID: 'NixCn84GdK2tySa5rB1V', timestamp: Date.now() };
        PubSub.publish('title_ID', message);
        console.log(`消息已发送: ${message.title_ID} at ${message.timestamp}`);
      },
      sendMessage2() {
        const message = { title_ID: '3MwAFlmNO8EKrpY5zjUd', timestamp: Date.now() };
        PubSub.publish('title_ID', message);
        console.log(`消息已发送: ${message.title_ID} at ${message.timestamp}`);
      },
      sendMessage3() {
        const message = { title_ID: 'lU2wvHSZq7m43xiVroBc', timestamp: Date.now() };
        PubSub.publish('title_ID', message);
        console.log(`消息已发送: ${message.title_ID} at ${message.timestamp}`);
      },
      receiveMessage(msg, data) {
        if (data.timestamp > this.latestTimestamp) {
          this.latestMessage = data.title_ID;
          this.latestTimestamp = data.timestamp;
          console.log(`接收到的新消息: ${data.title_ID} at ${data.timestamp}`);
        }
      }
    },
    mounted() {
      this.token = PubSub.subscribe('title_ID', this.receiveMessage);
    },
    beforeDestroy() {
      PubSub.unsubscribe(this.token);
    }
  }
  </script>
  