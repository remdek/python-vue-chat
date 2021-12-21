<template>
  <div class="container">
    <div class="chat">
      <div class="user-label"
           v-if="user_type">
        Вы {{ user_type === 'student' ? 'студент' : 'менеджер' }}
      </div>
      <!--      Приветствие-->
      <div v-if="!user_type" class="hello">
        <h1>Добро пожаловать в чат</h1>
        <p>Пожалуйста, выберите, кто вы:</p>
        <div>
          <input type="radio" value="manager" v-model="user_type">Менеджер
          <input type="radio" value="student" v-model="user_type">Ученик
        </div>
      </div>

<!--      Списко сообщений-->
      <div class="messages" v-if="user_type">
        <MsgComponent :msg="msg" :class="{'align-right' : msg.user !== $store.state.user.id}"
                      v-for="(msg, idx) in messages"
                      :key="idx"/>
      </div>

<!--      Выбор пользователя и предмета-->
      <div class="action-block" v-if="user_type">
        <hr>
        <SelectBlockComponent/>
        <ActionComponent/>
      </div>
    </div>


  </div>
</template>

<script>
import {defineAsyncComponent} from 'vue'
import MsgComponent from "@/components/MsgComponent";

const ActionComponent =
    defineAsyncComponent(() => import("@/components/ActionComponent.vue"));
const SelectBlockComponent =
    defineAsyncComponent(() => import("@/components/SelectBlockComponent.vue"));


export default {
  name: 'App',
  components: {MsgComponent, SelectBlockComponent, ActionComponent},
  created() {
    let socket = new WebSocket('ws://localhost:8000/ws/chat')
    socket.onmessage = (e) => {
      const data = JSON.parse(e.data)
      if (data.status === 'init-data') {
        console.log("Прилетел список предметов и юзеров", data)
        this.$store.commit('SET_OBJ', {name: 'lessons', value: JSON.parse(data.lessons)})
        this.$store.commit('SET_OBJ', {name: 'users', value: JSON.parse(data.users)})
      } else if (data.status === 'chat') {
        console.log('Это чат', data)
        const messages = JSON.parse(JSON.stringify(this.messages))
        messages.push(data)
        this.$store.commit('SET_OBJ', {name: 'messages', 'value': messages})
      } else if (data.status === 'init-messages') {
        console.log('Прилетели сообщения этого чата и пользователя', JSON.parse(data.messages))
        this.$store.commit('SET_OBJ', {name: 'messages', value: JSON.parse(data.messages)})
      }
    }
    socket.onopen = (e) => {
      console.log("open", e)
    }
    socket.onerror = (e) => {
      console.log("error", e)
    }
    socket.onclose = (e) => {
      console.log("close", e)
    }
    this.$store.commit('SET_OBJ', {name: 'socket', value: socket})
  },
  watch: {
    user_type() {
      this.$store.commit('SET_OBJ', {name: 'user_type', value: this.user_type})
    }
  },
  computed: {
    messages() {
      return this.$store.state.messages
    }
  },
  data() {
    return {
      user_type: null
    }
  }

}
</script>

<style lang="scss">
@import "./assets/styles";

.chat {
  position: relative;
  width: 600px;
  height: 100%;
  background: #FFFFFF;
}

.hello {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
  height: 100vh;
}


.messages, .action-block {
  padding: 10px;
}

.messages {
  display: flex;
  flex-direction: column;
  justify-content: end;
  position: absolute;
  bottom: 250px;
  height:80%;
  overflow-x: auto;
  margin: 30px;
  width: 87%;
  .align-right {
    align-self: end;
  }

}

.action-block {
  position: absolute;
  bottom:20px;
  //background: #cccccc;
  width: 100%;
}

</style>
