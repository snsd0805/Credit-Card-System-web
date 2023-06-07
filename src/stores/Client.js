import { defineStore } from 'pinia'

export const useClientStore = defineStore('Client', {
  state () {
    return {
      address: '',
      linked: false
    }
  }
})
