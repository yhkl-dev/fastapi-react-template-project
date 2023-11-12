import React from "react";
import { Layout, Breadcrumb } from "antd";
import { Outlet } from "react-router-dom";

const { Content } = Layout;

function DefaultLayoutContent() {
  return (
    <Content
      className="site-layout"
      style={{ padding: "0 20px", overflow: "auto" }}
    >
      <Breadcrumb style={{ margin: "0px 0" }}>
        <Breadcrumb.Item>Home</Breadcrumb.Item>
        <Breadcrumb.Item>ServiceAccount</Breadcrumb.Item>
      </Breadcrumb>
      <Outlet />
    </Content>
  );
}

export default DefaultLayoutContent;
