import type { ReactNode } from 'react'
import Markdown from 'markdown-to-jsx'

interface Message {
	content: string
	role: 'user' | 'assistant'
}

interface ChatMessageProps {
	message: Message
}

interface ChatListProps {
	children?: ReactNode
	messages: Message[]
}

function ChatMessage({ message }: ChatMessageProps) {
	if (message.role === 'user') {
		return (
			<div className='flex w-full justify-end'>
				<div className='max-w-[75%] rounded-2xl rounded-br-sm bg-teal-900 px-5 py-3 text-teal-50 shadow-xl'>
					{message.content}
				</div>
			</div>
		)
	} else if (message.role === 'assistant') {
		return (
			<div className='[&_ol]:list-inside [&_ol]:list-decimal [&_ul]:list-inside [&_ul]:list-disc'>
				<Markdown
					options={{ forceBlock: true }}
					className='flex flex-col gap-3'
				>
					{message.content}
				</Markdown>
			</div>
		)
	}
}

function ChatList({ children, messages }: ChatListProps) {
	return (
		<div className='relative flex h-auto w-full flex-col gap-8 overflow-y-auto rounded-xl px-7 py-11 pb-29'>
			{messages.map((message, i) => (
				<ChatMessage key={i} message={message} />
			))}
			{children}
		</div>
	)
}

export { type Message, ChatMessage, ChatList }
