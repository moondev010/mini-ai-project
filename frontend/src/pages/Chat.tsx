import { useEffect, useRef, useState } from 'react'

import InputBar from '../components/InputBar'
import MessageArea from '../components/MessageArea'
import SendButton from '../components/SendButton'
import { ChatList, ChatMessage, type Message } from '../components/ChatMessage'

import useChat from '../hooks/userChat'

function Chat() {
	const {
		isStreaming,
		streamingMessage,
		messages,
		sendMessage,
		appendMessages,
	} = useChat({
		url: 'ws://localhost:8000/chat',
	})
	const [prompt, setPrompt] = useState('')
	const bottomRef = useRef<HTMLDivElement | null>(null)

	useEffect(() => {
		const controller = new AbortController()

		const fetchData = async () => {
			try {
				const response = await fetch('http://localhost:8000/messages/all', {
					signal: controller.signal,
				})

				if (!response.ok) return

				const result: Message[] = await response.json()

				appendMessages(result)
			} catch (err) {
				if ((err as Error).name !== 'AbortError') {
					console.error('Message retrieval has failed')
				}
			}
		}

		fetchData()

		return () => controller.abort()
	}, [appendMessages])

	useEffect(() => {
		bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
	}, [messages, streamingMessage])

	return (
		<main className='flex h-dvh w-full justify-center px-5 py-6'>
			<div className='relative flex h-full w-full max-w-xl flex-col justify-end rounded-xl border-2 border-teal-300 bg-teal-100 shadow-xl'>
				<ChatList messages={messages}>
					{streamingMessage !== null && (
						<ChatMessage
							message={{ role: 'assistant', content: streamingMessage }}
						/>
					)}
					<div ref={bottomRef}></div>
				</ChatList>
				<InputBar>
					<MessageArea
						placeholder='Mensaje'
						value={prompt}
						onChange={(e) => setPrompt(e.target.value)}
					/>
					<SendButton
						disabled={isStreaming || !prompt.trim()}
						onClick={() => {
							sendMessage(prompt)
							setPrompt('')
						}}
					/>
				</InputBar>
			</div>
		</main>
	)
}

export default Chat
