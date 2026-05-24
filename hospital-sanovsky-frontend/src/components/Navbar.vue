<template>
    <nav class="navbar navbar-expand-lg bg-white shadow-sm py-3">
      <div class="container">
        <a class="navbar-brand fw-bold fs-4" href="#">Sanovsky</a>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse justify-content-end" id="navbarNav">
          <ul class="navbar-nav">
            <li class="nav-item mx-2">
              <router-link class="nav-link text-dark" to="/especialidades">Especialidades</router-link>
            </li>
            <li class="nav-item mx-2">
              <router-link class="nav-link text-dark" to="/medicos">Médicos</router-link>
            </li>
            <li class="nav-item mx-2">
              <router-link class="nav-link text-dark" to="/faq">Preguntas Frecuentes</router-link>
            </li>
          </ul>
          <div class="d-flex flex-column flex-lg-row">
            <button
              v-if="!isAuthenticated"
              class="btn btn-outline-dark me-2 mt-2 mt-lg-0"
              @click="router.push('/login')"
            >
              Iniciar Sesión
            </button>
            <button
              v-if="isAuthenticated"
              class="btn btn-danger mt-2 mt-lg-0"
              @click="logout"
            >
              Cerrar Sesión
            </button>
          </div>
        </div>
      </div>
    </nav>
  </template>
<script setup>
import { useRouter } from 'vue-router'
import { ref, onMounted } from 'vue'

const router = useRouter()

const isAuthenticated = ref(false)

onMounted(() => {
  isAuthenticated.value = !!localStorage.getItem('authUser')
})

const logout = () => {
  localStorage.removeItem('authUser')
  router.push('/login')
}
</script>