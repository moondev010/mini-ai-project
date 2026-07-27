import { useState } from 'react'

import InputBar from '../components/InputBar'
import MessageArea from '../components/MessageArea'
import SendButton from '../components/SendButton'
import { ChatList, ChatMessage } from '../components/ChatMessage'

import useChat from '../hooks/userChat'

function Chat() {
	const { isStreaming, streamingMessage, messages, sendMessage } = useChat({
		url: 'ws://localhost:8000/chat',
	})
	const [prompt, setPrompt] = useState('')

	return (
		<main className='flex h-dvh w-full justify-center px-5 py-6'>
			<div className='relative flex h-full w-full max-w-xl flex-col justify-end rounded-xl border-2 border-teal-300 bg-teal-100 shadow-xl'>
				<ChatList messages={messages}>
					{streamingMessage !== null && (
						<ChatMessage
							message={{ role: 'assistant', content: streamingMessage }}
						/>
					)}
				</ChatList>
				<InputBar>
					<MessageArea
						placeholder='Mensaje'
						onChange={(e) => setPrompt(e.target.value)}
					/>
					<SendButton
						disabled={isStreaming || !prompt.trim()}
						onClick={() => sendMessage(prompt)}
					/>
				</InputBar>
			</div>
		</main>
	)
}

export default Chat
