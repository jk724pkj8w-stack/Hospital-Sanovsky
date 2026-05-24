<template>
  <div class="container my-4">
    <h1 class="mb-3 text-success">Preguntas Frecuentes</h1>
    <p class="mb-4">Aquí encontrarás respuestas a las preguntas más comunes de nuestros usuarios.</p>

    <div class="accordion" id="faqAccordion">
      <div class="accordion-item" v-for="(item, index) in preguntas" :key="index">
        <h2 class="accordion-header" :id="'heading' + index">
          <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse"
                  :data-bs-target="'#collapse' + index" aria-expanded="false"
                  :aria-controls="'collapse' + index">
            {{ item.pregunta }}
          </button>
        </h2>
        <div :id="'collapse' + index" class="accordion-collapse collapse"
             :aria-labelledby="'heading' + index" data-bs-parent="#faqAccordion">
          <div class="accordion-body">
            {{ item.respuesta }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Faq',
  data() {
    return {
      preguntas: [
        {
          pregunta: '¿Cómo puedo agendar una cita médica?',
          respuesta: 'Puedes agendar una cita ingresando a la sección "Agendar Cita" y completando el formulario con tus datos.'
        },
        {
          pregunta: '¿Puedo cancelar una cita agendada?',
          respuesta: 'Sí, puedes cancelar una cita desde tu perfil o llamando a nuestra línea de atención.'
        },
        {
          pregunta: '¿Qué especialidades médicas ofrecen?',
          respuesta: 'Ofrecemos diversas especialidades como cardiología, pediatría, neurología, entre otras.'
        },
        {
          pregunta: '¿Qué necesito llevar para mi consulta médica?',
          respuesta: 'Debes llevar tu identificación oficial, comprobante de cita y cualquier estudio médico previo que tengas.'
        },
        {
          pregunta: '¿Cómo puedo consultar mis citas agendadas?',
          respuesta: 'Puedes consultar tus citas ingresando a tu perfil de usuario en la sección de citas.'
        },
        {
          pregunta: '¿Atienden emergencias?',
          respuesta: 'Sí, contamos con atención de emergencias las 24 horas, los 7 días de la semana.'
        },
        {
          pregunta: '¿Puedo elegir al médico que me atenderá?',
          respuesta: 'Sí, puedes elegir al médico disponible de tu preferencia al momento de agendar la cita.'
        }
      ]
    };
  }
}
</script>

<style scoped>
.container {
  max-width: 800px;
}
</style>