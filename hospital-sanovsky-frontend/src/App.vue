<template>
  <nav class="navbar navbar-expand-lg navbar-white bg-white shadow-sm">
    <div class="container">
      <a class="navbar-brand d-flex align-items-center" href="#">
        <img src="./assets/image.jpg" alt="Hospital Sanovsky Logo" style="height: 80px; width: auto; object-fit: contain; margin-right: 24px;">
        <span class="visually-hidden">Hospital Sanovsky</span>
      </a>
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse justify-content-end" id="navbarNav">
        <ul class="navbar-nav">
          <li class="nav-item">
            <router-link class="nav-link" to="/especialidades">Especialidades</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/medicos">Médicos</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/faq">Preguntas Frecuentes</router-link>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="#" @click.prevent="iniciarSesion">Inicio</a>
          </li>
          <li class="nav-item d-flex align-items-center text-white fw-bold" v-if="isAuthenticated">
            <span class="nav-link">Hola, {{ userName }}</span>
          </li>
          <li class="nav-item" v-if="isAuthenticated">
            <a class="nav-link" href="#" @click.prevent="cerrarSesion">Cerrar Sesión</a>
          </li>
        </ul>
      </div>
    </div>
  </nav>

  <div class="app">
    <section class="text-center py-5 bg-light">
      <h1 class="display-4 fw-bold">Bienvenido al Hospital Sanovsky</h1>
      <p class="lead">Tecnología y atención médica de primer nivel</p>
    </section>
    <router-view></router-view>
  </div>
</template>

<script>
import { getDocs, collection } from 'firebase/firestore';
import { db } from './firebase';
import { watch } from 'vue'
import { useRoute } from 'vue-router'

export default {
  data() {
    return {
      isAuthenticated: false,
      userName: '',
      doctorNombre: ''
    }
  },
  mounted() {
    this.isAuthenticated = !!localStorage.getItem('authUser');
    if (this.isAuthenticated) {
      const user = JSON.parse(localStorage.getItem('authUser'))
      this.userName = user?.displayName || 'Usuario'
    }
    const route = useRoute();
    watch(() => route.path, () => {
      this.isAuthenticated = !!localStorage.getItem('authUser');
      if (this.isAuthenticated) {
        const user = JSON.parse(localStorage.getItem('authUser'))
        this.userName = user?.displayName || 'Usuario'
      } else {
        this.userName = ''
      }
    });
    watch(() => route.query, () => {
      this.doctorNombre = route.query.doctor_nombre || '';
    });
  },
  methods: {
    async obtenerPacientes() {
      try {
        const querySnapshot = await getDocs(collection(db, 'pacientes'));
        this.pacientes = querySnapshot.docs.map(doc => {
          const data = doc.data();
          return {
            id: doc.id,
            nombre: data.nombre || '',
            apellidoPaterno: data.apellidoPaterno || '',
            apellidoMaterno: data.apellidoMaterno || '',
            edad: data.edad || '',
            alergias: data.alergias || ''
          };
        });
      } catch (error) {
        console.error("Error al obtener pacientes:", error);
      }
    },
    iniciarSesion() {
      console.log("Iniciar sesión");
      this.$router.push("/login");
    },
    cerrarSesion() {
      localStorage.removeItem('authUser');
      this.isAuthenticated = false;
      this.userName = ''
      this.$router.push('/login');
    }
  },
  created() {
    this.obtenerPacientes();
  }
}
</script>

<style scoped>
/* Barra de navegación con fondo claro y texto oscuro */
.navbar {
  background-color: #ffffff; /* Fondo claro */
  font-family: 'Arial', sans-serif;
  padding: 10px 0;
}

.navbar-brand {
  display: flex;
  align-items: center;
  color: #222222; /* Texto oscuro */
  font-size: 1.75rem;
  font-weight: bold;
  letter-spacing: 1px;
}

.navbar-nav {
  gap: 15px;
}

.navbar-nav .nav-link {
  color: #333333; /* Texto oscuro */
  font-size: 1.1rem;
  font-weight: 500;
  padding: 12px 24px;
  letter-spacing: 0.5px;
}

.navbar-nav .nav-link:hover {
  color: #4CAF50; /* Verde Celta */
  text-decoration: none;
}

.navbar-toggler-icon {
  background-color: #333333; /* Icono oscuro */
}

.nav-item.d-flex.align-items-center {
  font-size: 1.1rem;
}

.navbar-nav .nav-link.text-danger {
  color: #222222;
}

.navbar-nav .nav-link.text-danger:hover {
  color: #D32F2F;
}

.app {
  background-color: #F8F9FA;
}

.text-center h1 {
  font-size: 2.5rem;
  font-weight: bold;
  color: #111211; /* Verde Celta */
}

.text-center p {
  font-size: 1.25rem;
  color: #555;
}

/* Visually hidden utility for accessibility */
.visually-hidden {
  position: absolute !important;
  height: 1px; width: 1px;
  overflow: hidden;
  clip: rect(1px, 1px, 1px, 1px);
  white-space: nowrap;
}

@media (max-width: 768px) {
  .navbar-nav {
    text-align: center;
  }
  .navbar-toggler {
    border-color: #4CAF50;
  }
}

</style>