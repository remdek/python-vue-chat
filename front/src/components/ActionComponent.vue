<template>
  <div class="action">
    <label for="msg">Сообщение</label>
    <input type="text" id="msg"
           v-model="msg"
           :disabled="!$store.state.user"
           @keydown.enter="sendMessage"
    >
    <button :disabled="!$store.state.user"
            @click="sendMessage">Отправить
    </button>
  </div>
</template>

<script>
export default {
  name: "Action.component",
  data() {
    return {
      msg: '',
      user: 0,

    }
  },
  methods: {
    async sendMessage() {
      const data = JSON.stringify({
        message: this.msg,
        lesson: this.$store.state.lesson.id,
        user: this.$store.state.user.id,
        type: 'chat'
      })
      await this.$store.state.socket.send(data)
      this.msg = ''
    }
  }
}
</script>

<style scoped>


</style>