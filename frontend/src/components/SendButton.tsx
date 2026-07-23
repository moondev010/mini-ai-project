import { SendHorizontal } from 'lucide-react'

interface SendButtonProps {
	onClick?: () => {}
}

function SendButton({ onClick }: SendButtonProps) {
	return (
		<button
			onClick={onClick}
			className='grid h-17 w-17 place-content-center rounded-full bg-teal-900 text-gray-100 shadow-xl transition-colors hover:bg-teal-700 active:bg-teal-600'
		>
			<SendHorizontal />
		</button>
	)
}

export default SendButton
