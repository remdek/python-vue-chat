<template>
  <label for="user">Пользователь</label>
  <select id="user"
          v-model="user_id">
    <option value="0" disabled>Выберите пользователя</option>
    <option :value="user.id"
            v-for="(user, idx) in users"
            :key="idx">
      {{ user.f_name }}</option>

  </select>

  <label for="lesson">Предмет</label>
  <select id="lesson"
          v-model="lesson_id"
          :disabled="!user_id"
          @change="updateLesson">
    <option value="0" disabled>Выберите предмет</option>
    <option :value="lesson.id"
            v-for="(lesson, idx) in access_lessons"
            :key="idx">
      {{ lesson.name }}</option>

  </select>

</template>

<script>
export default {
  name: "SelectBlockComponent",
  computed: {
    users() {
      return  this.$store.state.users.filter(u => this.$store.state.user_type === u.type)
    },
    access_lessons() {
      if (this.user_id) {
        const currentUser = this.users.find(u => u.id === this.user_id)
        this.$store.commit('SET_OBJ', {name: 'user', value: currentUser})
        return this.$store.state.lessons.filter(l => currentUser.access.includes(l.id))
      }
      return []

    }
  },
  data() {
    return {
      lesson_id: 0,
      user_id: 0,
      lessons: []
    }
  },
  methods: {
    async updateLesson() {
      const currentLesson = this.access_lessons.find(l => l.id === this.lesson_id)
      this.$store.commit('SET_OBJ', {name: 'lesson', value: currentLesson})
      const data = JSON.stringify({
        message: '',
        lesson: this.lesson_id,
        user: this.$store.state.user.id,
        type: 'customization'
      })
      await this.$store.state.socket.send(data)
    }
  }
}
</script>

<style scoped>

</style>