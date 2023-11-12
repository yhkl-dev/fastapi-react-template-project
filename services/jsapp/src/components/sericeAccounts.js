import React, { Fragment, useEffect, useState } from "react";
import {
  Button,
  Form,
  Spin,
  Pagination,
  Input,
  Space,
  Table,
  Modal,
  Checkbox,
} from "antd";
import {
  getServiceAccount,
  createServiceAccount,
  updateServiceAccount,
  deleteServiceAccount,
} from "../apis/serviceAccount";
import { ExclamationCircleFilled } from "@ant-design/icons";
import AddOrUpdateServiceAccount from "./serviceaccount/addOrUpdateServiceAccount";
import dayjs from "dayjs";

const { confirm } = Modal;

const renderBoolean = (value) => {
  return <Checkbox checked={value}></Checkbox>;
};

const COLUMNS = [
  {
    title: "AccountName",
    dataIndex: "account_name",
    key: "account_name",
    fixed: "left",
  },
  {
    title: "Account information",
    children: [
      {
        title: "Domain",
        dataIndex: "domain",
        key: "domain",
      },
      {
        title: "EmailAddress",
        dataIndex: "email_address",
        key: "",
      },
      {
        title: "Account Expiration Date",
        dataIndex: "account_expiration_date",
        key: "account_expiration_date",
        render: (date) => dayjs(date).format("YYYY-MM-DD HH:mm:ss"),
      },
      {
        title: "ABI password rule",
        dataIndex: "abi_password_rule",
        key: "abi_password_rule",
        render: (value) => renderBoolean(value),
      },
      {
        title: "Password Expiration date",
        dataIndex: "password_expiration_date",
        key: "password_expiration_date",
        render: (date) => dayjs(date).format("YYYY-MM-DD HH:mm:ss"),
      },
    ],
  },
  {
    title: "User information",
    children: [
      {
        title: "Owner Email",
        dataIndex: "owner_email",
        key: "owner_email",
      },
      {
        title: "Applicant email",
        dataIndex: "applicant_email",
        key: "applicant_email",
      },
      {
        title: "End Users email",
        dataIndex: "end_user_email",
        key: "end_user_email",
      },
    ],
  },
  {
    title: "Permission information",
    children: [
      {
        title: "Group",
        dataIndex: "group",
        key: "group",
      },
      {
        title: "Role",
        dataIndex: "role",
        key: "role",
      },
      {
        title: "Account permission",
        dataIndex: "account_permission",
        key: "account_permission",
      },
    ],
  },
  {
    title: "Account usage information",
    children: [
      {
        title: "Server Name",
        dataIndex: "server_name",
        key: "server_name",
      },
      {
        title: "IP",
        dataIndex: "ip",
        key: "ip",
      },
      {
        title: "Service name",
        dataIndex: "service_name",
        key: "service_name",
      },
      {
        title: "Application name",
        dataIndex: "application_name",
        key: "application_name",
      },
      {
        title: "Save the password in script",
        dataIndex: "save_the_password_in_script",
        key: "save_the_password_in_script",
        render: (value) => renderBoolean(value),
      },
      {
        title: "Script name",
        dataIndex: "script_name",
        key: "script_name",
      },
      {
        title: "Multiple apps",
        dataIndex: "multiple_apps",
        key: "multiple_apps",
      },
    ],
  },
  {
    title: "Account Managed information",
    children: [
      {
        title: "Account for different Application",
        dataIndex: "account_for_different_application",
        key: "account_for_different_application",
        render: (value) => renderBoolean(value),
      },
      {
        title: "Managed system description",
        dataIndex: "managed_system_description",
        key: "managed_system_description",
      },
      {
        title: "managed Account description",
        dataIndex: "managed_account_description",
        key: "managed_account_description",
      },
      {
        title: "Change the password periodically",
        dataIndex: "change_the_password_periodically",
        key: "change_the_password_periodically",
        render: (value) => renderBoolean(value),
      },
      {
        title: "Account_Automanage",
        dataIndex: "account_automanage",
        key: "account_automanage",
        render: (value) => renderBoolean(value),
      },
    ],
  },
];

function SericeAccounts() {
  const [total, setTotal] = useState(0);
  const [createOpen, setCreateOpen] = useState(false);
  const [updateOpen, setUpdateOpen] = useState(false);
  const [current, setCurrent] = useState(1);
  const [loading, setLoading] = useState(true);
  const [serviceAccounts, setServiceAccounts] = useState([]);
  const [currentData, setCurrentData] = useState({});
  const [form] = Form.useForm();
  const serviceAccountsColumns = [
    ...COLUMNS,
    {
      title: "Operation",
      key: "action",
      width: 200,
      fixed: "right",
      render: (_, record) => (
        <Space size="middle">
          <Button
            type="link"
            onClick={() => {
              console.log(">>>", record);
              setUpdateOpen(true);
              setCurrentData(record);
            }}
            style={{}}
          >
            Update
          </Button>
          <Button
            danger
            type="text"
            onClick={() => {
              showConfirm(record);
            }}
          >
            Delete
          </Button>
        </Space>
      ),
    },
  ];

  const onSearch = (value) => {
    getServiceAccounts(value);
  };

  const showConfirm = (record) => {
    confirm({
      title: "Do you want to delete this item?",
      icon: <ExclamationCircleFilled />,
      content: record.management_address,
      onOk() {
        deleteServiceAccount(record.id).then(() => {
          reLoading();
        });
      },
      onCancel() {
        console.log("Cancel delete");
      },
    });
  };

  const onChange = (page) => {
    setCurrent(page);
    getServiceAccounts({
      page: current,
    });
  };
  const onCreate = (values) => {
    createServiceAccount(values).then(() => {
      reLoading();
    });
    setCreateOpen(false);
  };

  const onUpdate = (values) => {
    console.log("update", values);
    updateServiceAccount(currentData.id, values).then((res) => {
      reLoading();
    });
    setUpdateOpen(false);
  };

  const getServiceAccounts = (params) => {
    getServiceAccount(params).then((response) => {
      setServiceAccounts(response.data.items);
      setTotal(response.data.total);
      setLoading(false);
    });
  };

  const reLoading = () => {
    setLoading(true);
    getServiceAccounts({ page: current });
  };

  useEffect(() => {
    getServiceAccounts({ page: current });
  }, [current]);

  if (loading) {
    return <Spin />;
  } else {
    return (
      <Fragment>
        <Space style={{ marginBottom: "20px" }}>
          <Form layout="inline" form={form}>
            <Form.Item label="Account Name" name="account_name">
              <Input placeholder="input account name" allowClear />
            </Form.Item>
            <Form.Item label="IP address" name="ip">
              <Input placeholder="input ip address" allowClear />
            </Form.Item>
            <Form.Item label="service name" name="service_name">
              <Input placeholder="input service name" allowClear />
            </Form.Item>
            <Form.Item>
              <Button
                type="primary"
                onClick={() => {
                  form
                    .validateFields()
                    .then((values) => {
                      onSearch(values);
                    })
                    .catch((info) => {
                      console.log("Validate Failed:", info);
                    });
                }}
              >
                Search
              </Button>
            </Form.Item>
            {/* <Form.Item>
              <Button
                type="primary"
                onClick={() => {
                  setCreateOpen(true);
                }}
              >
                New Service Account
              </Button>
            </Form.Item> */}
            <Form.Item>
              <Button onClick={reLoading}>refresh</Button>
            </Form.Item>
          </Form>
        </Space>
        <AddOrUpdateServiceAccount
          open={createOpen}
          onCreate={onCreate}
          onCancel={() => {
            setCreateOpen(false);
          }}
          okText={"CREATE"}
          operation={"Create"}
        ></AddOrUpdateServiceAccount>
        <AddOrUpdateServiceAccount
          open={updateOpen}
          onCreate={onUpdate}
          data={currentData}
          onCancel={() => {
            setUpdateOpen(false);
            setCurrentData({});
          }}
          okText={"UPDATE"}
          operation={"Update"}
        ></AddOrUpdateServiceAccount>
        <Table
          dataSource={serviceAccounts}
          columns={serviceAccountsColumns}
          pagination={false}
          scroll={{ x: "max-content" }}
          size="small"
        />
        <Pagination
          defaultCurrent={current}
          pageSizeOptions={["10"]}
          total={total}
          onChange={onChange}
        ></Pagination>
      </Fragment>
    );
  }
}

export default SericeAccounts;
