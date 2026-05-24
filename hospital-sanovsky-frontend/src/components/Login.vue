<template>
  <div class="d-flex align-items-center justify-content-center vh-100 bg-light">
    <div class="card p-4 shadow" style="width: 350px;">
      <h3 class="text-center mb-3">Inicia Sesión</h3>
      <form @submit.prevent="login">
        <div class="mb-3">
          <label for="email" class="form-label">Correo</label>
          <input v-model="email" type="email" class="form-control" id="email" required />
        </div>
        <div class="mb-3">
          <label for="password" class="form-label">Contraseña</label>
          <input v-model="password" type="password" class="form-control" id="password" required />
        </div>
        <button type="submit" class="btn btn-dark w-100">Entrar</button>
      </form>
      <div class="text-center mt-3">
        <p class="mb-1">¿No tienes cuenta?</p>
        <router-link to="/register" class="btn btn-outline-primary w-100">Registrarse</router-link>
      </div>
      <div v-if="isAuthenticated">
        <button class="btn btn-outline-secondary w-100 mt-2" @click="logout">Cerrar sesión</button>
      </div>
      <div v-if="loginError" class="alert alert-danger mt-3">
        {{ loginError }}
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { signInWithEmailAndPassword } from 'firebase/auth'
import { auth } from '../firebase'
import { useRouter } from 'vue-router'

const email = ref('')
const password = ref('')
const loginError = ref('')
const router = useRouter()
const isAuthenticated = ref(!!localStorage.getItem('authUser'))

onMounted(() => {
  if (isAuthenticated.value) {
    router.push('/dashboard')
  }
})

onMounted(() => {
  const justRegistered = localStorage.getItem('justRegistered')
  if (justRegistered) {
    localStorage.removeItem('justRegistered')
    router.push('/dashboard')
  }
})

const login = async () => {
  try {
    const userCredential = await signInWithEmailAndPassword(auth, email.value, password.value)
    console.log('Usuario autenticado:', userCredential.user)
    localStorage.setItem('authUser', JSON.stringify(userCredential.user))
    isAuthenticated.value = true
    router.push('/dashboard')  // Usar router directamente
  } catch (error) {
    console.error('Error al iniciar sesión:', error.message)
    loginError.value = 'Correo o contraseña incorrectos.'  // Mostrar el mensaje de error en la interfaz
  }
}

const logout = () => {
  localStorage.removeItem('authUser')
  isAuthenticated.value = false
  router.push('/login')
}
</script>