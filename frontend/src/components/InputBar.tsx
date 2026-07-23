import { type ReactNode } from 'react'

interface InputBarProps {
	children: ReactNode
}

function InputBar({ children }: InputBarProps) {
	return (
		<div className='absolute bottom-0 left-0 right-0 flex w-full items-center gap-3 px-6 py-6 bg-linear-to-t rounded-xl from-teal-50 to-transparent'>
			{children}
		</div>
	)
}

export default InputBar
