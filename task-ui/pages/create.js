import { useEffect, useState } from "react";
import { useRouter } from "next/router";
import { createTask, getUsers } from "../utils/api";

export default function CreateTask() {
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [status, setStatus] = useState("Todo");
  const [deadline, setDeadline] = useState("");
  const [assigneeId, setAssigneeId] = useState("");
  const [users, setUsers] = useState([]);
  const router = useRouter();
  const token = typeof window !== "undefined" ? localStorage.getItem("token") : null;

  useEffect(() => {
    if (!token) router.push("/");
    const fetchUsers = async () => setUsers(await getUsers(token));
    fetchUsers();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    await createTask({ title, description, status, deadline, assignee_id: parseInt(assigneeId) }, token);
    router.push("/dashboard");
  };

  return (
    <div style={{ padding: "20px" }}>
      <h1>Create Task</h1>
      <form onSubmit={handleSubmit}>
        <input type="text" placeholder="Title" value={title} onChange={e => setTitle(e.target.value)} required />
        <textarea placeholder="Description" value={description} onChange={e => setDescription(e.target.value)} required />
        <select value={status} onChange={e => setStatus(e.target.value)}>
          <option value="Todo">Todo</option>
          <option value="In Progress">In Progress</option>
          <option value="Done">Done</option>
        </select>
        <input type="date" value={deadline} onChange={e => setDeadline(e.target.value)} required />
        <select value={assigneeId} onChange={e => setAssigneeId(e.target.value)} required>
          <option value="">Select Assignee</option>
          {users.map(u => <option key={u.id} value={u.id}>{u.username}</option>)}
        </select>
        <button type="submit">Create</button>
      </form>
    </div>
  );
}
