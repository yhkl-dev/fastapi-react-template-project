import { Fragment, useEffect, useState } from "react";
import { Table, Space, Button, Spin } from "antd";

function Tasks() {
  const [current, setCurrent] = useState({});
  const [error, setError] = useState(null);
  const tasks = [
    {
      no: 1,
      task_name: "ecs",
    },
    {
      no: 2,
      task_name: "rds",
    },
    {
      no: 3,
      task_name: "kms",
    },
    {
      no: 4,
      task_name: "oss",
    },
    {
      no: 5,
      task_name: "ssl",
    },
    {
      no: 6,
      task_name: "ssl",
    },
    {
      no: 7,
      task_name: "sls",
    },
    {
      no: 8,
      task_name: "network",
    },
    {
      no: 9,
      task_name: "check_data_legality",
    },
  ];

  const columns = [
    {
      title: "No",
      dataIndex: "no",
      key: "no",
    },
    {
      title: "Task Name",
      dataIndex: "task_name",
      key: "task_name",
    },
    {
      title: "Action",
      key: "action",
      render: (_, record) => (
        <Space size="middle">
          <Button
            type="link"
            onClick={() => {
              setCurrent(record);
              runTasks();
            }}
            style={{
              marginBottom: "10px",
            }}
          >
            Run tasks
          </Button>
        </Space>
      ),
    },
  ];

  const runTasks = () => {
    const headers = new Headers();
    headers.append("Content-Type", "application/json");
    const requestOpions = {
      method: "POST",
      body: JSON.stringify({
        task_name: current.task_name,
      }),
      headers: headers,
    };
    fetch(
      process.env.REACT_APP_API_ENDPOINT + "/inventory/run_sync_task",
      requestOpions
    )
      .then((response) => response.json())
      .then((data) => {
        if (data.code !== 200) {
          console.log("error: ", data.message);
          setError(data.message);
        } else {
          console.log(data);
        }
      });
  };

  useEffect(() => {}, []);
  if (error !== null) {
    return <div>error</div>;
  } else {
    return (
      <Fragment>
        <Table dataSource={tasks} columns={columns} />
      </Fragment>
    );
  }
}

export default Tasks;
