import React, { Fragment, useCallback, useEffect, useMemo } from "react";
import { Modal, Form, Input, DatePicker, Checkbox } from "antd";
import dayjs from "dayjs";

function AddOrUpdateServiceAccount({
  open,
  onCreate,
  onCancel,
  okText,
  operation,
  data,
}) {
  const title = operation + " Service Account";
  const [form] = Form.useForm();

  const initData = useMemo(() => {
    if (data) {
      const return_data = {
        ...data,
        password_expiration_date:
          data.password_expiration_date &&
          dayjs(data.password_expiration_date, "YYYY-MM-DDTHH:mm:ss").isValid()
            ? dayjs(data.password_expiration_date, "YYYY-MM-DDTHH:mm:ss")
            : null,
        account_expiration_date:
          data.account_expiration_date &&
          dayjs(data.account_expiration_date, "YYYY-MM-DDTHH:mm:ss").isValid()
            ? dayjs(data.account_expiration_date, "YYYY-MM-DDTHH:mm:ss")
            : null,
      };
      return return_data;
    }
    return data;
  }, [data]);

  const handleOk = useCallback(() => {
    form
      .validateFields()
      .then((values) => {
        onCreate(values);
        form.resetFields();
      })
      .catch((info) => {
        console.log("Validate Failed:", info);
      });
  }, [form, onCreate]);

  useEffect(() => {
    form.setFieldsValue(initData);
  }, [data, form]);

  return (
    <Fragment>
      <Modal
        open={open}
        title={title}
        okText={okText}
        cancelText="Cancel"
        onCancel={() => {
          form.resetFields();
          onCancel();
        }}
        width={800}
        onOk={handleOk}
      >
        <Form
          labelCol={{
            span: 8,
          }}
          wrapperCol={{
            span: 16,
          }}
          style={{
            maxWidth: 700,
          }}
          form={form}
          name="form_in_modal"
          initialValues={initData}
        >
          {/* AccountName */}
          <Form.Item
            label="AccountName"
            name="account_name"
            rules={[{ required: true, message: "Please input AccountName!" }]}
          >
            <Input />
          </Form.Item>

          {/* Account information */}
          <Form.Item
            label="Domain"
            name="domain"
            rules={[{ required: true, message: "Please input Domain!" }]}
          >
            <Input />
          </Form.Item>
          <Form.Item
            label="EmailAddress"
            name="email_address"
            rules={[{ required: true, message: "Please input EmailAddress!" }]}
          >
            <Input />
          </Form.Item>
          <Form.Item
            label="Account Expiration Date"
            name="account_expiration_date"
            rules={[
              {
                required: true,
                message: "Please input Account Expiration Date!",
              },
            ]}
          >
            <DatePicker showTime format="YYYY-MM-DD HH:mm:ss" />
          </Form.Item>
          <Form.Item
            label="ABI password rule"
            name="abi_password_rule"
            valuePropName="checked"
            rules={[
              { required: true, message: "Please input ABI password rule!" },
            ]}
          >
            <Checkbox>Yes</Checkbox>
          </Form.Item>
          <Form.Item
            label="Password Expiration date"
            name="password_expiration_date"
            rules={[
              {
                required: true,
                message: "Please input Password Expiration date!",
              },
            ]}
          >
            <DatePicker showTime format="YYYY-MM-DD HH:mm:ss" />
          </Form.Item>

          {/* User information */}
          <Form.Item
            label="Owner Email"
            name="owner_email"
            rules={[{ required: true, message: "Please input Owner Email!" }]}
          >
            <Input />
          </Form.Item>
          <Form.Item
            label="Applicant email"
            name="applicant_email"
            rules={[
              { required: true, message: "Please input Applicant email!" },
            ]}
          >
            <Input />
          </Form.Item>
          <Form.Item
            label="End Users email"
            name="end_user_email"
            rules={[
              { required: true, message: "Please input End Users email!" },
            ]}
          >
            <Input />
          </Form.Item>

          {/* Permission information */}
          <Form.Item
            label="Group"
            name="group"
            rules={[{ required: true, message: "Please input Group!" }]}
          >
            <Input />
          </Form.Item>
          <Form.Item
            label="Role"
            name="role"
            rules={[{ required: true, message: "Please input Role!" }]}
          >
            <Input />
          </Form.Item>
          <Form.Item
            label="Account permission"
            name="account_permission"
            rules={[
              { required: true, message: "Please input Account permission!" },
            ]}
          >
            <Input />
          </Form.Item>

          {/* Account usage information */}
          <Form.Item
            label="Server Name"
            name="server_name"
            rules={[{ required: true, message: "Please input Server Name!" }]}
          >
            <Input />
          </Form.Item>
          <Form.Item
            label="IP"
            name="ip"
            rules={[{ required: true, message: "Please input IP!" }]}
          >
            <Input />
          </Form.Item>
          <Form.Item
            label="Service name"
            name="service_name"
            rules={[{ required: true, message: "Please input Service name!" }]}
          >
            <Input />
          </Form.Item>
          <Form.Item
            label="Application name"
            name="application_name"
            rules={[
              { required: true, message: "Please input Application name!" },
            ]}
          >
            <Input />
          </Form.Item>
          <Form.Item
            label="Save the password in script"
            name="save_the_password_in_script"
            valuePropName="checked"
            rules={[
              {
                required: true,
                message: "Please input Save the password in script!",
              },
            ]}
          >
            <Checkbox>Yes</Checkbox>
          </Form.Item>
          <Form.Item
            label="Script name"
            name="script_name"
            rules={[{ required: true, message: "Please input Script name!" }]}
          >
            <Input />
          </Form.Item>
          <Form.Item
            label="Multiple apps"
            name="multiple_apps"
            rules={[{ required: true, message: "Please input Multiple apps!" }]}
          >
            <Input />
          </Form.Item>

          {/* Account Managed information */}
          <Form.Item
            label="Account for different Application"
            name="account_for_different_application"
            rules={[
              {
                required: true,
                message: "Please input Account for different Application!",
              },
            ]}
          >
            <Input />
          </Form.Item>
          <Form.Item
            label="Managed system description"
            name="managed_system_description"
            rules={[
              {
                required: true,
                message: "Please input Managed system description!",
              },
            ]}
          >
            <Input />
          </Form.Item>
          <Form.Item
            label="Managed Account description"
            name="managed_account_description"
            rules={[
              {
                required: true,
                message: "Please input Managed Account description!",
              },
            ]}
          >
            <Input />
          </Form.Item>
          <Form.Item
            label="Change the password periodically"
            name="change_the_password_periodically"
            valuePropName="checked"
            rules={[
              {
                required: true,
                message: "Please input Change the password periodically!",
              },
            ]}
          >
            <Checkbox>Yes</Checkbox>
          </Form.Item>
          <Form.Item
            label="Account Automanage"
            name="account_automanage"
            valuePropName="checked"
            rules={[
              { required: true, message: "Please input Account Automanage!" },
            ]}
          >
            <Checkbox>Yes</Checkbox>
          </Form.Item>
        </Form>
      </Modal>
    </Fragment>
  );
}

export default AddOrUpdateServiceAccount;
