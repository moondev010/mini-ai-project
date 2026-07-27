import { twMerge } from 'tailwind-merge'
import { SendHorizontal } from 'lucide-react'

interface SendButtonProps {
	disabled?: boolean
	onClick?: () => void
}

function SendButton({ disabled, onClick }: SendButtonProps) {
	return (
		<button
			onClick={onClick}
			className={twMerge(
				'grid h-17 w-17 place-content-center rounded-full bg-teal-900 text-gray-100 shadow-xl transition-colors hover:bg-teal-700 active:bg-teal-600',
				disabled ? 'opacity-20 hover:bg-teal-900 active:bg-teal-900' : '',
			)}
			disabled={disabled}
		>
			<SendHorizontal />
		</button>
	)
}

export default SendButton
