<template>
  <div class="chat-container">
    <img class="avatar" :src="avatar" alt="Avatar" />
    <div class="chat-box" ref="chatBox" v-html="renderedText"></div>
  </div>
</template>
<script>
import MarkdownIt from 'markdown-it';

export default {
  name: 'ChatBox',
  data() {
    return {
      avatar: 'https://statics.moonshot.cn/kimi-chat/static/01.0245bc9d.png',
      text: '',
      typingSpeed: 10,
      // 用来显示的数据
      displayedText: '',
      // 用来显示的markdown文本 实时修改 displayedText
      renderedText: ''
    };
  },
  mounted() {
    // this.fetchText();
    this.fetchTextStream();
  },
  methods: {
    fetchText() {
      this.$axios.get('http://10.12.44.190:8000/getComments/?student_id=00cbf05221bb479e66c3')
        .then(response => {
          this.text = JSON.parse(response.data).text;
          console.log("#####this.text#######:", this.text)
          this.showText();
        })
        .catch(error => {
          console.error("There was an error!", error);
        });
    },
    fetchTextStream() {
      let _this = this;

      fetch('http://10.12.44.190:8000/getComments_stream/?student_id=00cbf05221bb479e66c3', {
        method: 'GET',
      }).then(response => {
        const reader = response.body.getReader();
        const decoder = new TextDecoder('utf-8');

        function processStreamResult(result) {
          const chunk = decoder.decode(result.value, { stream: !result.done });
          // 可以接收到异步数据！
          console.log('Received chunk:', chunk);
          this.text += chunk;
          this.showText();


          if (!result.done) {
            reader.read().then(processStreamResult);
          }
        }
        reader.read().then(processStreamResult);
      })
        .catch(error => {
          console.error('Error:', error);
        });

    },
    showText() {
      let index = 0;
      const textLength = this.text.length;
      const interval = setInterval(() => {
        this.displayedText += this.text.charAt(index);
        index++;
        this.scrollToBottom();
        if (index === textLength) {
          clearInterval(interval);
        }
      }, this.typingSpeed);
    },
    scrollToBottom() {
      const chatBox = this.$refs.chatBox;
      chatBox.scrollTop = chatBox.scrollHeight;
    }
  },
  // 监听要显示文本的增加 及时变为markdown文本 添加到显示文本中
  watch: {
    displayedText(newVal) {
      const md = new MarkdownIt();
      // this.renderedText = md.render(newVal);
      this.renderedText = newVal;
    }
  }
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
  max-width: 500px;
  max-height: 650px;
  overflow-y: auto;
  word-break: break-word;
  white-space: pre-wrap;
  font-family: Arial, sans-serif;
}
</style>