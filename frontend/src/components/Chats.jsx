import {useState, useEffect } from 'react';
import { useQuery } from "react-query";
import { Link, useParams } from "react-router-dom";
import ScrollContainer from './ScrollContainer';
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
		return <ChatCardContainer messages={data.messages} />
	}

	return <h2>loading...</h2>
}
  
function ChatCardContainer({ messages }){
	return (
		<div className="chat-card-container gap-5 py-5">
			<h2 className='text-lg' >Messages</h2>
			<MessageList messages={messages} />
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
		<div className="message-list-item">
			<div className="message-header" >
				<div className="message-owner-id">
					{message.user_id}
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

export default Chats