import {createStore} from 'vuex'

export default createStore({
    state: {
        user_type: null,
        user: 0,
        users: [],
        lesson: 0,
        lessons: [],
        socket: null,
        messages: []
    },
    mutations: {
        SET_OBJ(state, payload) {
            if (payload.key) {
                state[payload.name][payload.key] = payload.value
            } else {
                state[payload.name] = payload.value
            }
        }


    },
    actions: {},
    modules: {}
})
