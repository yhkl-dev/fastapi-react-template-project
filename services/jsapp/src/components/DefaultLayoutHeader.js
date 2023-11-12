import React from "react";
import { Layout, Space, Button } from "antd";
import { MenuFoldOutlined, MenuUnfoldOutlined } from "@ant-design/icons";
import { useSelector } from "react-redux";

const { Header } = Layout;

function DefaultLayoutHeader({ collapsed, setCollapsed, colorBgContainer }) {
  const response = useSelector((state) => state.response);

  return (
    <Header
      style={{
        padding: 0,
        background: colorBgContainer,
      }}
    >
      <Space style={{ display: "flex", justifyContent: "space-between" }}>
        <Button
          type="text"
          icon={collapsed ? <MenuUnfoldOutlined /> : <MenuFoldOutlined />}
          onClick={() => setCollapsed(!collapsed)}
          style={{
            fontSize: "16px",
            width: 64,
            height: 64,
          }}
        />
        <div>{response?.userName}</div>
      </Space>
    </Header>
  );
}

export default DefaultLayoutHeader;
