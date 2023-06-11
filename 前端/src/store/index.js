import { createStore } from 'vuex'

export default createStore({
    state: {
        login:0,
        showSearch:true,
        reFresh:false,
    },
    mutations: {
        login(state){
            console.log("vuex收到了")
            reFresh = true
        },
        logout(state){
            reFresh = false
        }
    },
    actions: {

    },
    modules: {
        
    }
})

