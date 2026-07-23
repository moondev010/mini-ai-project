import { type Message } from '../components/ChatMessage'

const longMessageExampleList: Message[] = [
	{
		id: 'msg-1',
		content: '¿Qué puedes hacer tú?',
		role: 'user',
	},
	{
		id: 'msg-2',
		content:
			'Este es un *mensaje motivacional* de parte de ***Flowy***, tu pequeño asistente de salud mental. \n 1. Primer elemento \n 2. Segundo elemento',
		role: 'assistant',
	},
	{
		id: 'msg-3',
		content:
			'Quiero saber cómo me puedes ayudar. Este es un mensaje un poco más largo para ver bien cómo funciona esto cuando se trata de ajustar el tamaño.',
		role: 'user',
	},
	{
		id: 'msg-4',
		content:
			'**Tal vez tú en realidad no quieres eso**. Aunque es imposible ver qué es lo que está pasando ahí, ¿sabes?',
		role: 'assistant',
	},
	{
		id: 'msg-5',
		content: '¿Qué onda? Últimamente me siento muy estresado con la escuela.',
		role: 'user',
	},
	{
		id: 'msg-6',
		content:
			'Órale, lamento escuchar eso. **El estrés escolar es súper común**, ¿qué tal si platicamos un poco sobre qué es lo que más te agobia? \n 1. Las tareas \n 2. Los exámenes \n 3. La presión de los papás',
		role: 'assistant',
	},
	{
		id: 'msg-7',
		content:
			'Creo que son los exámenes, siento que nunca voy a estar preparado.',
		role: 'user',
	},
	{
		id: 'msg-8',
		content:
			'Eso que sientes se llama *ansiedad anticipatoria* y es más común de lo que crees. ¿Te gustaría que armemos juntos un plan de estudio sencillo para que no se te acumule todo al final?',
		role: 'assistant',
	},
	{
		id: 'msg-9',
		content: 'Sí, por favor. La verdad no sé ni por dónde empezar.',
		role: 'user',
	},
	{
		id: 'msg-10',
		content:
			'No te preocupes, vamos paso a paso. \n 1. Elige una sola materia para hoy \n 2. Estudia en bloques de 25 minutos con descansos de 5 \n 3. Anota tus dudas para resolverlas después \n\n ¿Con cuál materia quieres empezar?',
		role: 'assistant',
	},
	{
		id: 'msg-11',
		content: 'Con matemáticas, es la que más se me dificulta.',
		role: 'user',
	},
	{
		id: 'msg-12',
		content:
			'**Perfecto, empecemos por ahí.** Recuerda que no pasa nada si al principio te cuesta trabajo, lo importante es la constancia y no la perfección.',
		role: 'assistant',
	},
	{
		id: 'msg-13',
		content:
			'Gracias, Flowy. La verdad hablar contigo ya me hizo sentir un poco mejor.',
		role: 'user',
	},
	{
		id: 'msg-14',
		content:
			'Me da mucho gusto escuchar eso. Aquí ando para lo que necesites, sin juzgar y sin prisas.',
		role: 'assistant',
	},
	{
		id: 'msg-15',
		content:
			'Oye, ¿tú puedes ayudarme también cuando me siento triste sin motivo aparente?',
		role: 'user',
	},
	{
		id: 'msg-16',
		content:
			'Claro que sí. A veces la tristeza aparece sin una razón clara y **está bien sentirla así**. ¿Quieres contarme desde cuándo te has sentido así?',
		role: 'assistant',
	},
	{
		id: 'msg-17',
		content: 'Desde hace como dos semanas, no tengo ganas de hacer nada.',
		role: 'user',
	},
	{
		id: 'msg-18',
		content:
			'Eso que describes puede ser señal de que tu cuerpo y tu mente necesitan un descanso más profundo. \n 1. ¿Cómo has dormido últimamente? \n 2. ¿Has podido comer bien? \n 3. ¿Sales un poco al día, aunque sea a caminar?',
		role: 'assistant',
	},
	{
		id: 'msg-19',
		content: 'La verdad duermo muy mal y casi no salgo de mi cuarto.',
		role: 'user',
	},
	{
		id: 'msg-20',
		content:
			'Gracias por confiarme eso. **Pequeños cambios pueden hacer una gran diferencia**, como abrir la cortina en la mañana o dar una vuelta corta a la cuadra. Si esto se prolonga, también sería bueno platicarlo con un profesional. ¿Cómo te suena empezar con algo chiquito hoy mismo?',
		role: 'assistant',
	},
	{
		id: 'msg-21',
		content: 'Me suena bien, voy a intentar salir aunque sea diez minutos.',
		role: 'user',
	},
	{
		id: 'msg-22',
		content:
			'¡Así se habla! Ese primer paso, aunque parezca pequeño, ya cuenta muchísimo.',
		role: 'assistant',
	},
	{
		id: 'msg-23',
		content:
			'Oye Flowy, ¿y si un día ya no quiero hablar de nada? ¿Igual puedo escribirte?',
		role: 'user',
	},
	{
		id: 'msg-24',
		content:
			'Por supuesto que sí. No tienes que hablar de nada en específico, aquí puedes solo *estar* y desahogarte cuando gustes, sin explicaciones ni compromisos.',
		role: 'assistant',
	},
]

const shortMessageExampleList: Message[] = [
	{
		id: 'msg-1',
		content: '¿Qué puedes hacer tú?',
		role: 'user',
	},
	{
		id: 'msg-2',
		content:
			'Este es un *mensaje motivacional* de parte de ***Flowy***, tu pequeño asistente de salud mental. \n 1. Primer elemento \n 2. Segundo elemento',
		role: 'assistant',
	},
	{
		id: 'msg-3',
		content:
			'Quiero saber cómo me puedes ayudar. Este es un mensaje un poco más largo para ver bien cómo funciona esto cuando se trata de ajustar el tamaño.',
		role: 'user',
	},
	{
		id: 'msg-4',
		content:
			'**Tal vez tú en realidad no quieres eso**. Aunque es imposible ver qué es lo que está pasando ahí, ¿sabes?',
		role: 'assistant',
	},
]

export { longMessageExampleList, shortMessageExampleList }
