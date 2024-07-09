<template>
  <div class="chat-container">
    <img class="avatar" :src="avatar" alt="Avatar" />
    <div class="chat-box" ref="chatBox" v-html="renderedText"></div>
  </div>
</template>

<script>
import MarkdownIt from 'markdown-it';
import { mapGetters } from 'vuex';
import PubSub from 'pubsub-js';

export default {
  name: 'ChatBox',
  data() {
    return {
      avatar: 'https://statics.moonshot.cn/kimi-chat/static/01.0245bc9d.png',
      text: '',
      typingSpeed: 10,
      displayedText: '',
      renderedText: '',
      requestQueue: [], // 队列来存储请求ID
      isFetching: false, // 当前是否正在进行请求
    };
  },
  mounted() {
    this.subscriptionToken = PubSub.subscribe('studentId', (msg, value) => {
      this.addToQueue(value);
    });
  },
  computed: {
    ...mapGetters(['studentId']),
  },
  created() {
    this.addToQueue(this.studentId);
  },
  methods: {
    addToQueue(studentId) {
      this.requestQueue.push(studentId);
      this.processQueue();
    },
    processQueue() {
      if (this.isFetching || this.requestQueue.length === 0) return;

      this.isFetching = true;
      const studentId = this.requestQueue.shift();
      this.fetchTextStream(studentId);
    },
    fetchTextStream(studentId) {
      fetch(`http://10.12.44.190:8000/getComments_stream/?student_id=${studentId}`, {
        method: 'GET',
      })
          .then(response => {
            const reader = response.body.getReader();
            const decoder = new TextDecoder('utf-8');

            const processStreamResult = (result) => {
              const chunk = decoder.decode(result.value, { stream: !result.done });
              console.log('Received chunk:', chunk);
              this.displayedText += chunk;
              this.renderMarkdown();
              this.scrollToBottom();

              if (!result.done) {
                reader.read().then(processStreamResult);
              } else {
                this.isFetching = false; // 请求完成
                this.processQueue(); // 处理下一个请求
              }
            };

            reader.read().then(processStreamResult);
          })
          .catch(error => {
            this.isFetching = false; // 确保请求错误时也能继续处理队列
            if (error.name === 'AbortError') {
              console.log('Fetch aborted');
            } else {
              console.error('Error:', error);
            }
            this.processQueue(); // 处理下一个请求
          });
    },
    renderMarkdown() {
      const md = new MarkdownIt({ html: true, linkify: true, typographer: true, breaks: true });
      this.renderedText = md.render(this.displayedText);
    },
    scrollToBottom() {
      const chatBox = this.$refs.chatBox;
      chatBox.scrollTop = chatBox.scrollHeight;
    },
  },
};
</script>

<style scoped>
.chat-container {
  display: flex;
  align-items: flex-start;
}

.avatar {
  width: 50px;
  height: 50px;
  margin-right: 10px;
}

.chat-box {
  background-color: #f0f0f0;
  border-radius: 10px;
  padding: 10px;
  max-width: 580px;
  max-height: 700px;
  overflow-y: auto;
  word-break: break-word;
  font-family: Arial, sans-serif;
}
</style>
