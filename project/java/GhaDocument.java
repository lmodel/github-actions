package example;

/* metamodel_version: 1.12.0 */
/* version: 2026-10-28 */
import java.net.URI;
import java.time.LocalDate;
import java.time.LocalTime;
import java.time.ZonedDateTime;
import java.util.List;
import lombok.*;

/**
  A document that holds the workflows, actions, rulesets and required status checks of one or more repositories.
**/
@Data
@EqualsAndHashCode(callSuper=false)
public class GhaDocument  {

  private List<GhaWorkflow> workflows;
  private List<GhaReusableWorkflow> reusableWorkflows;
  private List<GhaAction> actions;
  private List<GhaRepositoryRuleset> rulesets;
  private List<GhaRequiredStatusCheck> requiredChecks;


}