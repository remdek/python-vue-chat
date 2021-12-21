<template>
  <div class="msg-wrapper">
    <span class="name">{{ user.f_name }}</span>
    <span class="msg"
          :class="$store.state.user.id === msg.user
          ? 'color-green' : 'color-gray'">
      {{ msg.text }}
    </span>
  </div>
</template>

<script>
export default {
  name: "MsgComponent",
  props: ['msg'],
  computed: {
    users() {
      return this.$store.state.users
    },
    user() {
      return this.users.find(u => u.id === this.msg.user)
    }
  }
}
</script>

<style scoped lang="scss">
.msg-wrapper {
  margin: 10px 0 10px 0;

  .name {
    display: block;
    font-size: 9px;
    font-weight: bolder;

  }
}

.msg {
  border: 1px solid #000;
  border-radius: 4px;
  padding: 5px;
  color: #000;
  font-size: 12px;
}

  .color-gray {
    background: #cccccc;
  }
  .color-green {
    background: #8cc68c;
  }
</style>