import {useState, useEffect } from 'react';
import { useMutation, useQueryClient } from 'react-query';
import { useQuery } from "react-query";
import { Link, useParams, useNavigate } from "react-router-dom";
import ScrollContainer from './ScrollContainer';
import { useAuth } from '../context/auth';
import "./Chats.css";

function Chats({}){
	const { chatId } = useParams();
	return (
		<div className="chats-page" >
			<ChatListContainer />
			<ChatCardQueryContainer chatId={chatId}/>
		</div>
	)
}

function ChatListItem({ chat }){
	const [date, setDate] = useState();

	useEffect(() => {
		formatDate();
	}), [];

	const formatDate = () => {
		setDate(new Date(chat.created_at).toDateString());
	}

	return (
		<Link key={chat.id} to={`/chats/${chat.id}`} className="chat-list-item">
			<div className="chat-item-name">
				{chat.name}
			</div>
			<div className="chat-item-date">
				<p>Created at: {date}</p>
			</div>
		</Link>
	)
}

function ChatList({ chats }) {
	return (
		<div className="chat-list" >
			{chats.map((chat) => (
				<ChatListItem key={chat.id} chat={chat}/>
			))}
		</div>
	)
}

function ChatListContainer({}) {
	const { data } = useQuery({
		queryKey: ["chats"],
		queryFn: () => (
			fetch("http://localhost:8000/chats")
			.then(response => response.json())
		),
	});

	if (data?.chats) {
		return (
			<div className='py-5'>
				<h2 className='text-lg text-center'>All Chats</h2>
				<div className="chat-list-container py-5 px-2 gap-5 my-5 rounded border-2 h-fit">
					<ChatList chats={data.chats} /> 
				</div>
			</div>
		)
	}
}

function ChatCardQueryContainer({ chatId }) {
	if (!chatId) {
		return (
			<div className='flex flex-col w-1/2 items-center justify-start border-2 border-purple-300 rounded-md my-16'>
				<h2 className='p-10 text-xl'>
					Select a chat
				</h2>
			</div>
		);
	}

	const { data } = useQuery({
		queryKey: ["messages", chatId],
		queryFn: () => (
		fetch(`http://127.0.0.1:8000/chats/${chatId}/messages`)
			.then((response) => response.json())
		),
	});

	if (data && data.messages) {
		return <ChatCardContainer messages={data.messages} chatId={chatId} />
	}

	return <h2>loading...</h2>
}
  
function ChatCardContainer({ messages, chatId }){
	return (
		<div className="flex flex-col flex-grow chat-card-container py-5 max-w-screen-sm">
			<h2 className='text-lg' >Messages</h2>
			<MessageList messages={messages} />
			<div className='flex flex-row justify-center items-center flex-grow w-full border-2 rounded-md border-purple-300 gap-3'>
				<NewMessageForm chatId={chatId}/>
			</div>
		</div>
	)
}

function MessageList({ messages }){
	return (
		<ScrollContainer>
			<div className="message-list">
				{messages.map((msg, id) => (
					<MessageListItem key={id++} message={msg}/>
					))}
			</div>
		</ScrollContainer>
	)
}

function MessageListItem({ message }){
	const [date, setDate] = useState();
	const [time, setTime] = useState();

	useEffect(() => {
		formatDate();
	}, [])

	const formatDate = () => {
		var datetime = new Date(message.created_at);
		setDate(datetime.toDateString());
		setTime(datetime.toLocaleTimeString());
	}

	return (
		<div className="message-list-item bg-gray-300">
			<div className="message-header" >
				<div className="message-owner-id">
					{message.user.username}
				</div>
				<div className="message-date">
					{date} - {time}
				</div>
			</div>
			<div className="message-content">
				{message.text}
			</div>
		</div>	
	)
}

function NewMessageForm({chatId}) {
	const [text, setText] = useState("");
	const { token } = useAuth();
	const queryClient = useQueryClient();
	const navigate = useNavigate();

	const mutation = useMutation({
		mutationFn: () => (
		  fetch(
			`http://127.0.0.1:8000/chats/${chatId}/messages`,
			{
			  method: "POST",
			  headers: {
				"Authorization": "Bearer " + token,
				"Content-Type": "application/json",
			  },
			  body: JSON.stringify({
				text,
			  }),
			},
		  ).then((response) => response.json())
		),
		onSuccess: () => {
		  queryClient.invalidateQueries({
			queryKey: ["messages", chatId],
		  });
		  setText("")
		  navigate(`/chats/${chatId}`);
		},
	  });

	const handleSubmit = (e) => {
		e.preventDefault();
		mutation.mutate();
	}

	return (
		<>
			<form onSubmit={handleSubmit} className='flex flex-grow items-center max-w-full'>
				<input type="text" placeholder='message' value={text} onChange={(e) => setText(e.target.value)} className='flex w-11/12 bg-gray-300 p-1 m-1 border rounded text-black'/>
				<button type="submit" className='p-1 mr-2 bg-purple-500 border rounded-lg h-2/3 flex justify-center items-center'>
					Send
				</button>
			</form>
		</>
	)
}

export default Chats