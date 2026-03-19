import { useState } from "react";
import { useTranslation } from "react-i18next";
import { I18nKey } from "#/i18n/declaration";
import { BrandButton } from "#/components/features/settings/brand-button";

export type RequestType = "saas" | "self-hosted";

interface InformationRequestFormProps {
  requestType: RequestType;
  onBack: () => void;
}

export function InformationRequestForm({
  requestType,
  onBack,
}: InformationRequestFormProps) {
  const { t } = useTranslation();
  const [formData, setFormData] = useState({
    name: "",
    email: "",
    company: "",
    message: "",
  });

  const handleInputChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>,
  ) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    // TODO: Implement form submission
    console.log("Form submitted:", { requestType, ...formData });
  };

  const title =
    requestType === "saas"
      ? t(I18nKey.ENTERPRISE$SAAS_TITLE)
      : t(I18nKey.ENTERPRISE$SELF_HOSTED_TITLE);

  return (
    <div
      data-testid="information-request-form"
      className="w-full max-w-md flex flex-col gap-6"
    >
      <div className="text-center">
        <h2 className="text-xl font-semibold text-white">{title}</h2>
        <p className="text-[#8C8C8C] mt-2">
          {t(I18nKey.ENTERPRISE$FORM_SUBTITLE)}
        </p>
      </div>

      <form onSubmit={handleSubmit} className="flex flex-col gap-4">
        <div className="flex flex-col gap-2">
          <label htmlFor="name" className="text-sm text-white">
            {t(I18nKey.ENTERPRISE$FORM_NAME_LABEL)}
          </label>
          <input
            type="text"
            id="name"
            name="name"
            value={formData.name}
            onChange={handleInputChange}
            required
            className="px-4 py-2.5 bg-[#0D0D0D] border border-[#242424] rounded-sm text-white placeholder-[#8C8C8C] focus:outline-none focus:border-[#404040]"
            placeholder={t(I18nKey.ENTERPRISE$FORM_NAME_PLACEHOLDER)}
          />
        </div>

        <div className="flex flex-col gap-2">
          <label htmlFor="email" className="text-sm text-white">
            {t(I18nKey.ENTERPRISE$FORM_EMAIL_LABEL)}
          </label>
          <input
            type="email"
            id="email"
            name="email"
            value={formData.email}
            onChange={handleInputChange}
            required
            className="px-4 py-2.5 bg-[#0D0D0D] border border-[#242424] rounded-sm text-white placeholder-[#8C8C8C] focus:outline-none focus:border-[#404040]"
            placeholder={t(I18nKey.ENTERPRISE$FORM_EMAIL_PLACEHOLDER)}
          />
        </div>

        <div className="flex flex-col gap-2">
          <label htmlFor="company" className="text-sm text-white">
            {t(I18nKey.ENTERPRISE$FORM_COMPANY_LABEL)}
          </label>
          <input
            type="text"
            id="company"
            name="company"
            value={formData.company}
            onChange={handleInputChange}
            required
            className="px-4 py-2.5 bg-[#0D0D0D] border border-[#242424] rounded-sm text-white placeholder-[#8C8C8C] focus:outline-none focus:border-[#404040]"
            placeholder={t(I18nKey.ENTERPRISE$FORM_COMPANY_PLACEHOLDER)}
          />
        </div>

        <div className="flex flex-col gap-2">
          <label htmlFor="message" className="text-sm text-white">
            {t(I18nKey.ENTERPRISE$FORM_MESSAGE_LABEL)}
          </label>
          <textarea
            id="message"
            name="message"
            value={formData.message}
            onChange={handleInputChange}
            rows={4}
            className="px-4 py-2.5 bg-[#0D0D0D] border border-[#242424] rounded-sm text-white placeholder-[#8C8C8C] focus:outline-none focus:border-[#404040] resize-none"
            placeholder={t(I18nKey.ENTERPRISE$FORM_MESSAGE_PLACEHOLDER)}
          />
        </div>

        <div className="flex flex-col gap-3 mt-4">
          <BrandButton
            type="submit"
            variant="primary"
            className="w-full px-6 py-2.5"
          >
            {t(I18nKey.ENTERPRISE$FORM_SUBMIT)}
          </BrandButton>
          <BrandButton
            type="button"
            variant="secondary"
            onClick={onBack}
            className="w-full px-6 py-2.5 bg-[#050505] text-white border border-[#242424] hover:bg-white hover:text-black"
          >
            {t(I18nKey.COMMON$BACK)}
          </BrandButton>
        </div>
      </form>
    </div>
  );
}
