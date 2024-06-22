<!-- <template>
  <div class="chat-container">
    <img class="avatar" :src="avatar" alt="Avatar" />
    <div class="chat-box" ref="chatBox" v-html="renderedText"></div>
  </div>
</template>
<script>
import { html } from 'd3';
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
          // 成功显示在前端页面！现在的问题是前端显示太快了，需要加一个延时显示
          _this.displayedText += chunk;
          // _this.text += chunk;
          // showText中慢慢将text倒入到displayedText中
          // _this.showText();
          _this.renderMarkdown();
          _this.scrollToBottom();

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
    // showText() {
    //   let index = 0;
    //   const textLength = this.text.length;
    //   const interval = setInterval(() => {
    //     this.displayedText += this.text.charAt(index);
    //     index++;
    //     this.scrollToBottom();
    //     if (index === textLength) {
    //       clearInterval(interval);
    //     }
    //   }, this.typingSpeed);
    //   // 导入到displayedText后，再进行markdown渲染
    //   this.renderMarkdown();
    //   this.scrollToBottom();
    // },
    renderMarkdown() {
      const md = new MarkdownIt({html: true, linkify: true, typographer: true, breaks: true});
      this.renderedText = md.render(this.displayedText);
      // this.renderedText = this.displayedText;
    },
    scrollToBottom() {
      const chatBox = this.$refs.chatBox;
      chatBox.scrollTop = chatBox.scrollHeight;
    }
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
  /* 下面两行代码导致间距过大 */
  word-break: break-word;
  /* white-space: pre-wrap;  */
  font-family: Arial, sans-serif;
}

/* 调整标题与正文之间的间距 */
.chat-box h1, .chat-box h2, .chat-box h3, .chat-box h4, .chat-box h5, .chat-box h6 {
  margin-top: 0.01em; /* 根据需要调整上边距 */
  margin-bottom: 0.01em; /* 根据需要调整下边距 */
}
</style> -->