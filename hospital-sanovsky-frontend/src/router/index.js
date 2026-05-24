import { createRouter, createWebHistory } from 'vue-router'
import Home from '../components/Home.vue'; 
import PacienteForm from '../components/PacienteForm.vue'
import RegistroEspecialista from '../views/RegistroEspecialista.vue'
import AgendarCita from '../views/AgendarCita.vue'
import Especialidades from '../views/Especialidades.vue'
import EspecialidadDetalle from '../views/EspecialidadDetalle.vue'
import Medicos from '../views/Medicos.vue'
import Faq from '../views/Faq.vue'
import Login from '../components/Login.vue'
import Register from '../components/Register.vue'
import Dashboard from '../views/Dashboard.vue'
import VerCitas from '../views/VerCitas.vue';

const routes = [
  {
    path: '/',
    name: 'home',
    component: Home
  },
  {
    path: '/registro-paciente',
    name: 'registro-paciente',
    component: PacienteForm
  },
  {
    path: '/registro-especialista',
    name: 'registro-especialista',
    component: RegistroEspecialista
  },
  {
    path: '/agendar-cita',
    name: 'agendar-cita',
    component: AgendarCita
  },
  {
    path: '/especialidades',
    name: 'especialidades',
    component: Especialidades
  },
  {
    path: '/especialidades/:id',
    name: 'especialidad-detalle',
    component: EspecialidadDetalle
  },
  {
    path: '/medicos',
    name: 'medicos',
    component: Medicos
  },
  {
    path: '/faq',
    name: 'faq',
    component: Faq
  },
  {
    path: '/login',  // Añadimos la ruta /login
    name: 'login',
    component: Login
  },
  {
    path: '/register', 
    name: 'register',
    component: Register
  },
  { path: '/dashboard',
    name: 'dashboard', 
    component: Dashboard 
  },
  {
  path: '/ver-citas',
  name: 'ver-citas',
  component: VerCitas
}
  
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

// Simulación de función de autenticación (puedes reemplazar esto con Firebase Auth o similar)
function isAuthenticated() {
  return !!localStorage.getItem('authUser'); // ejemplo simple: verificar si hay un usuario guardado
}

// Definir las rutas protegidas (requieren autenticación)
const protectedRoutes = [
  'registro-paciente',
  'registro-especialista',
  'agendar-cita'
];

router.beforeEach((to, from, next) => {
  if (protectedRoutes.includes(to.name) && !isAuthenticated()) {
    next({ name: 'login' });
  } else {
    next();
  }
});

export default router