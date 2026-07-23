import { useState } from 'react'

import InputBar from '../components/InputBar'
import MessageArea from '../components/MessageArea'
import SendButton from '../components/SendButton'
import { type Message, ChatList } from '../components/ChatMessage'

import { longMessageExampleList, /*shortMessageExampleList*/ } from '../lib/messageExamples'

function Chat() {
	const [messages] = useState<Message[]>(longMessageExampleList)

	return (
		<main className='flex h-dvh w-full justify-center px-5 py-6'>
			<div className='relative flex h-full w-full max-w-xl flex-col justify-end rounded-xl border-2 border-teal-300 bg-teal-100 shadow-xl'>
				<ChatList messages={messages} />
				<InputBar>
					<MessageArea placeholder='Mensaje' />
					<SendButton />
				</InputBar>
			</div>
		</main>
	)
}

export default Chat
