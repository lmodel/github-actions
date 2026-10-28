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
  An actor who may bypass a ruleset, and when.
**/
@Data
@EqualsAndHashCode(callSuper=false)
public class GhaBypassActor  {

  private Integer actorId;
  private String actorType;
  private String bypassMode;


}