import { useEffect, useState } from "react";
import { getTasks, getUsers, deleteTask } from "../utils/api";
import { useRouter } from "next/router";

export default function Dashboard() {
  const [tasks, setTasks] = useState([]);
  const [users, setUsers] = useState([]);
  const [filterUser, setFilterUser] = useState("");
  const [filterStatus, setFilterStatus] = useState("");
  const router = useRouter();
  const token = typeof window !== "undefined" ? localStorage.getItem("token") : null;

  useEffect(() => {
    if (!token) router.push("/");
    fetchData();
  }, []);

  const fetchData = async () => {
    const t = await getTasks(token);
    const u = await getUsers(token);
    setTasks(t);
    setUsers(u);
  };

  const handleDelete = async (id) => {
    await deleteTask(id, token);
    fetchData();
  };

  const filteredTasks = tasks.filter(t =>
    (filterUser ? t.assignee_id === parseInt(filterUser) : true) &&
    (filterStatus ? t.status === filterStatus : true)
  );

  return (
    <div style={{ padding: "20px" }}>
      <h1>Task Dashboard</h1>
      <button onClick={() => router.push("/create")}>Create Task</button>

      <div style={{ margin: "20px 0" }}>
        <select onChange={(e) => setFilterUser(e.target.value)}>
          <option value="">All Assignees</option>
          {users.map(u => <option key={u.id} value={u.id}>{u.username}</option>)}
        </select>
        <select onChange={(e) => setFilterStatus(e.target.value)}>
          <option value="">All Status</option>
          <option value="Todo">Todo</option>
          <option value="In Progress">In Progress</option>
          <option value="Done">Done</option>
        </select>
      </div>

      <table border="1" cellPadding="10">
        <thead>
          <tr>
            <th>ID</th>
            <th>Title</th>
            <th>Assignee</th>
            <th>Status</th>
            <th>Deadline</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {filteredTasks.map(task => (
            <tr key={task.id}>
              <td>{task.id}</td>
              <td>{task.title}</td>
              <td>{users.find(u => u.id === task.assignee_id)?.username || "-"}</td>
              <td>{task.status}</td>
              <td>{task.deadline}</td>
              <td>
                <button onClick={() => router.push(`/task/${task.id}`)}>Edit</button>
                <button onClick={() => handleDelete(task.id)}>Delete</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
