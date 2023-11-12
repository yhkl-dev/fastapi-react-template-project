import React from "react";
import { Form, Input, Button, Space } from "antd";
import { UserOutlined, LockOutlined } from "@ant-design/icons";
import "./login.css";

function Login() {
  const onFinish = (values) => {
    login(values.username, values.password);
  };

  const login = async (username, password) => {
    window.location.href = "http://localhost:5000/login-redirect";
  };

  return (
    <div className="login-form-container">
      <Form
        name="normal_login"
        className="login-form"
        initialValues={{ remember: true }}
        onFinish={onFinish}
      >
        <Form.Item name="username">
          <Input
            prefix={<UserOutlined className="site-form-item-icon" />}
            placeholder="用户名"
          />
        </Form.Item>
        <Form.Item name="password">
          <Input
            prefix={<LockOutlined className="site-form-item-icon" />}
            type="password"
            placeholder="密码"
          />
        </Form.Item>

        <Space>
          <Form.Item>
            <Button
              type="primary"
              htmlType="submit"
              className="login-form-button"
            >
              Login
            </Button>
          </Form.Item>
          <Form.Item>
            <Button
              type="primary"
              htmlType="submit"
              className="login-form-button"
            >
              SSO Login
            </Button>
          </Form.Item>
        </Space>
      </Form>
    </div>
  );
}

export default Login;
