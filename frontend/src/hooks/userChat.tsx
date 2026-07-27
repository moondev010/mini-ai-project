import { useState, useRef, useCallback } from 'react'

import { useWebSocket } from 'partysocket/react'
import type ReconnectingWebSocket from 'partysocket/ws'

import { type Message } from '../components/ChatMessage'

interface ReturnElements {
	socket: ReconnectingWebSocket
	isStreaming: boolean
	streamingMessage: string | null
	messages: Message[]
	sendMessage: (prompt: string) => void
}

interface UseChatArguments {
	url: string
	interval?: number
}

interface Chunk {
	type: 'part' | 'done' | 'error'
	content?: string
}

function useChat({ url, interval = 80 }: UseChatArguments): ReturnElements {
	const [messages, setMessages] = useState<Message[]>([])
	const [streamingMessage, setStreamingMessage] = useState<string | null>(null)
	const [isStreaming, setIsStreaming] = useState<boolean>(false)

	const intervalRef = useRef<ReturnType<typeof setInterval> | null>(null)
	const partialMessage = useRef('')

	const socket = useWebSocket(url, [], {
		onMessage(e) {
			const chunk: Chunk = JSON.parse(e.data)

			if (chunk.type === 'part') {
				if (chunk.content) partialMessage.current += chunk.content

				if (!intervalRef.current)
					intervalRef.current = setInterval(() => {
						setStreamingMessage(partialMessage.current)
					}, interval)
			} else if (chunk.type === 'done') {
				if (intervalRef.current) {
					clearInterval(intervalRef.current)
					intervalRef.current = null
				}

				const finalText = partialMessage.current
				setMessages((prev) => [
					...prev,
					{ role: 'assistant', content: finalText },
				])

				setStreamingMessage(null)
				setIsStreaming(false)
				partialMessage.current = ''
			}
		},
	})

	const sendMessage = useCallback(
		(prompt: string) => {
			const trimmed = prompt.trim()

			if (!trimmed || isStreaming) return

			setMessages((prev) => [...prev, { role: 'user', content: trimmed }])

			setIsStreaming(true)
			socket.send(JSON.stringify({ prompt: trimmed }))
		},
		[socket, isStreaming],
	)

	return { socket, isStreaming, streamingMessage, messages, sendMessage }
}

export default useChat
