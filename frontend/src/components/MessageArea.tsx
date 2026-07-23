interface MessageAreaProps {
	placeholder: string
	onChange?: () => {}
}

function MessageArea({ placeholder, onChange }: MessageAreaProps) {
	return (
		<div className='flex max-h-32 min-h-15 w-fit flex-1 items-center overflow-y-auto rounded-lg border-2 border-teal-300 bg-teal-50 px-4 shadow-lg/5'>
			<textarea
				onChange={onChange}
				rows={1}
				className='field-sizing-content max-h-full w-full resize-none overflow-y-auto border-none py-2 leading-normal outline-none'
				placeholder={placeholder}
			></textarea>
		</div>
	)
}

export default MessageArea
